<?php

/*
 * This file is part of the Symfony package.
 *
 * (c) Fabien Potencier <fabien@symfony.com>
 *
 * For the full copyright and license information, please view the LICENSE
 * file that was distributed with this source code.
 */

namespace Symfony\Flex\Command;

use Composer\Command\BaseCommand;
use Composer\Config;
use Symfony\Component\Console\Input\InputArgument;
use Symfony\Component\Console\Input\InputInterface;
use Symfony\Component\Console\Input\InputOption;
use Symfony\Component\Console\Output\OutputInterface;
use Symfony\Component\Dotenv\Dotenv;
use Symfony\Flex\Options;

class DumpEnvCommand extends BaseCommand
{
    private $config;
    private $options;

    public function __construct(Config $config, Options $options)
    {
        $this->config = $config;
        $this->options = $options;

        parent::__construct();
    }

    protected function configure()
    {
        $this->setName('symfony:dump-env')
            ->setAliases(['dump-env'])
            ->setDescription('Compiles .env files to .env.local.php.')
            ->setDefinition([
                new InputArgument('env', InputArgument::OPTIONAL, 'The application environment to dump .env files for - e.g. "prod".'),
            ])
            ->addOption('empty', null, InputOption::VALUE_NONE, 'Ignore the content of .env files')
        ;
    }

    protected function execute(InputInterface $input, OutputInterface $output): int
    {
        $runtime = $this->options->get('runtime') ?? [];
        $envKey = $runtime['env_var_name'] ?? 'APP_ENV';

        if ($env = $input->getArgument('env') ?? $runtime['env'] ?? null) {
            $_SERVER[$envKey] = $env;
        }

        $path = $this->options->get('root-dir').'/'.($runtime['dotenv_path'] ?? '.env');

        if (!$env || !$input->getOption('empty')) {
            $vars = $this->loadEnv($path, $env, $runtime);
            $env = $vars[$envKey];
        }

        if ($input->getOption('empty')) {
            $vars = [$envKey => $env];
        }

        $vars = var_export($vars, true);
        $vars = <<<EOF
<?php

// This file was generated by running "composer dump-env $env"

return $vars;

EOF;
        file_put_contents($path.'.local.php', $vars, \LOCK_EX);

        $this->getIO()->writeError('Successfully dumped .env files in <info>.env.local.php</>');

        return 0;
    }

    private function loadEnv(string $path, ?string $env, array $runtime): array
    {
        if (!file_exists($autoloadFile = $this->config->get('vendor-dir').'/autoload.php')) {
            throw new \RuntimeException(\sprintf('Please run "composer install" before running this command: "%s" not found.', $autoloadFile));
        }

        require $autoloadFile;

        if (!class_exists(Dotenv::class)) {
            throw new \RuntimeException('Please run "composer require symfony/dotenv" to load the ".env" files configuring the application.');
        }

        $envKey = $runtime['env_var_name'] ?? 'APP_ENV';
        $globalsBackup = [$_SERVER, $_ENV];
        unset($_SERVER[$envKey]);
        $_ENV = [$envKey => $env];
        $_SERVER['SYMFONY_DOTENV_VARS'] = implode(',', array_keys($_SERVER));
        putenv('SYMFONY_DOTENV_VARS='.$_SERVER['SYMFONY_DOTENV_VARS']);

        try {
            if (method_exists(Dotenv::class, 'usePutenv')) {
                $dotenv = new Dotenv();
            } else {
                $dotenv = new Dotenv(false);
            }

            if (!$env && file_exists($p = "$path.local")) {
                $env = $_ENV[$envKey] = $dotenv->parse(file_get_contents($p), $p)[$envKey] ?? null;
            }

            if (!$env) {
                throw new \RuntimeException(\sprintf('Please provide the name of the environment either by passing it as command line argument or by defining the "%s" variable in the ".env.local" file.', $envKey));
            }

            $testEnvs = $runtime['test_envs'] ?? ['test'];

            if (method_exists($dotenv, 'loadEnv')) {
                $dotenv->loadEnv($path, $envKey, 'dev', $testEnvs);
            } else {
                // fallback code in case your Dotenv component is not 4.2 or higher (when loadEnv() was added)
                $dotenv->load(file_exists($path) || !file_exists($p = "$path.dist") ? $path : $p);

                if (!\in_array($env, $testEnvs, true) && file_exists($p = "$path.local")) {
                    $dotenv->load($p);
                }

                if (file_exists($p = "$path.$env")) {
                    $dotenv->load($p);
                }

                if (file_exists($p = "$path.$env.local")) {
                    $dotenv->load($p);
                }
            }

            unset($_ENV['SYMFONY_DOTENV_VARS']);
            $env = $_ENV;
        } finally {
            list($_SERVER, $_ENV) = $globalsBackup;
        }

        return $env;
    }
}
