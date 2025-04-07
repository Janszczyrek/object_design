<?php

namespace App\Model;

use App\Entity\Product;
use Doctrine\ORM\EntityManagerInterface;
use Symfony\Component\Validator\Validator\ValidatorInterface;

class ProductModel
{
    private EntityManagerInterface $entityManager;
    private ValidatorInterface $validator;

    public function __construct(
        EntityManagerInterface $entityManager,
        ValidatorInterface $validator
    ) {
        $this->entityManager = $entityManager;
        $this->validator = $validator;
    }

    /**
     * Create a new product from data array
     * 
     * @param array $data
     * @return array|Product Returns Product on success, array of errors on failure
     */
    public function createProduct(array $data): array|Product
    {
        $product = new Product();
        $this->hydrateProduct($product, $data);
        
        $validationResult = $this->validateProduct($product);
        if (is_array($validationResult)) {
            return $validationResult;
        }
        
        $this->entityManager->persist($product);
        $this->entityManager->flush();
        
        return $product;
    }

    /**
     * Update an existing product from data array
     * 
     * @param Product $product
     * @param array $data
     * @return array|Product Returns Product on success, array of errors on failure
     */
    public function updateProduct(Product $product, array $data): array|Product
    {
        $this->hydrateProduct($product, $data);
        
        $validationResult = $this->validateProduct($product);
        if (is_array($validationResult)) {
            return $validationResult;
        }
        
        $this->entityManager->flush();
        
        return $product;
    }

    /**
     * Delete a product
     * 
     * @param Product $product
     * @return void
     */
    public function deleteProduct(Product $product): void
    {
        $this->entityManager->remove($product);
        $this->entityManager->flush();
    }

    /**
     * Set product properties from data array
     * 
     * @param Product $product
     * @param array $data
     * @return void
     */
    private function hydrateProduct(Product $product, array $data): void
    {
        if (isset($data['name'])) {
            $product->setName($data['name']);
        }
        
        if (isset($data['price'])) {
            $product->setPrice($data['price']);
        }
        
        if (isset($data['description'])) {
            $product->setDescription($data['description']);
        }
    }

    /**
     * Validate a product
     * 
     * @param Product $product
     * @return true|array Returns true on success, array of errors on failure
     */
    private function validateProduct(Product $product): bool|array
    {
        $errors = $this->validator->validate($product);
        
        if (count($errors) > 0) {
            $errorMessages = [];
            foreach ($errors as $error) {
                $errorMessages[$error->getPropertyPath()] = $error->getMessage();
            }
            return $errorMessages;
        }
        
        return true;
    }
}