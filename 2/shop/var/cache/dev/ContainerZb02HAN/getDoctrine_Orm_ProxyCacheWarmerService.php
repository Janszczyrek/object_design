<?php

namespace ContainerZb02HAN;

use Symfony\Component\DependencyInjection\Argument\RewindableGenerator;
use Symfony\Component\DependencyInjection\ContainerInterface;
use Symfony\Component\DependencyInjection\Exception\RuntimeException;

/**
 * @internal This class has been auto-generated by the Symfony Dependency Injection Component.
 */
class getDoctrine_Orm_ProxyCacheWarmerService extends App_KernelDevDebugContainer
{
    /**
     * Gets the private 'doctrine.orm.proxy_cache_warmer' shared service.
     *
     * @return \Symfony\Bridge\Doctrine\CacheWarmer\ProxyCacheWarmer
     */
    public static function do($container, $lazyLoad = true)
    {
        include_once \dirname(__DIR__, 4).'/vendor/symfony/http-kernel/CacheWarmer/CacheWarmerInterface.php';
        include_once \dirname(__DIR__, 4).'/vendor/symfony/doctrine-bridge/CacheWarmer/ProxyCacheWarmer.php';

        return $container->privates['doctrine.orm.proxy_cache_warmer'] = new \Symfony\Bridge\Doctrine\CacheWarmer\ProxyCacheWarmer(($container->services['doctrine'] ?? self::getDoctrineService($container)));
    }
}
