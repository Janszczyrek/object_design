<?php

namespace App\Controller;

use App\Entity\Product;
use App\Repository\ProductRepository;
use App\Model\ProductModel;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Attribute\Route;
use Symfony\Component\Serializer\SerializerInterface;

#[Route('/api/product')]
final class ProductController extends AbstractController
{
    private ProductModel $productModel;

    public function __construct(ProductModel $productModel)
    {
        $this->productModel = $productModel;
    }

    #[Route(name: 'app_product_index', methods: ['GET'])]
    public function index(ProductRepository $productRepository): JsonResponse
    {
        $products = $productRepository->findAll();
        return $this->json($products);
    }

    #[Route('/new', name: 'app_product_new', methods: ['POST'])]
    public function new(Request $request): JsonResponse
    {
        $data = json_decode($request->getContent(), true);
        
        if (json_last_error() !== JSON_ERROR_NONE) {
            return $this->json(['error' => 'Invalid JSON'], Response::HTTP_BAD_REQUEST);
        }
        
        $result = $this->productModel->createProduct($data);
        
        if (is_array($result)) {
            return $this->json(['errors' => $result], Response::HTTP_BAD_REQUEST);
        }
        
        return $this->json(
            $result,
            Response::HTTP_CREATED,
            ['Location' => $this->generateUrl('app_product_show', ['id' => $result->getId()])]
        );
    }

    #[Route('/{id}', name: 'app_product_show', methods: ['GET'])]
    public function show(Product $product): JsonResponse
    {
        return $this->json($product);
    }

    #[Route('/{id}/edit', name: 'app_product_edit', methods: ['PUT'])]
    public function edit(Request $request, Product $product): JsonResponse
    {
        $data = json_decode($request->getContent(), true);
        
        if (json_last_error() !== JSON_ERROR_NONE) {
            return $this->json(['error' => 'Invalid JSON'], Response::HTTP_BAD_REQUEST);
        }
        
        $result = $this->productModel->updateProduct($product, $data);
        
        if (is_array($result)) {
            return $this->json(['errors' => $result], Response::HTTP_BAD_REQUEST);
        }
        
        return $this->json($result);
    }

    #[Route('/{id}', name: 'app_product_delete', methods: ['DELETE'])]
    public function delete(Product $product): JsonResponse
    {
        $this->productModel->deleteProduct($product);
        return $this->json(null, Response::HTTP_NO_CONTENT);
    }
}
