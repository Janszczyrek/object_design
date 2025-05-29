import Vapor

struct ProductController: RouteCollection {
    func boot(routes: any RoutesBuilder) throws {
        let productsRoute = routes.grouped("products")
        productsRoute.get(use: index)
        productsRoute.post(use: create)
    }

    func index(req: Request) throws -> EventLoopFuture<View> {
        return Product.query(on: req.db).all().flatMap { products in
            let context = ["products": products]
            return req.view.render("products", context)
        }
    }
    
    func create(req: Request) throws -> EventLoopFuture<Response> {
        let product = try req.content.decode(Product.self)
        return product.save(on: req.db).map { _ in
            return req.redirect(to: "/products")
        }
    }

    func update(req: Request) throws -> EventLoopFuture<Response> {
        let product = try req.content.decode(Product.self)
        return Product.find(req.parameters.get("id"), on: req.db)
            .unwrap(or: Abort(.notFound))
            .flatMap { existingProduct in
                existingProduct.name = product.name
                existingProduct.description = product.description
                existingProduct.price = product.price
                return existingProduct.save(on: req.db).map {
                    req.redirect(to: "/products")
                }
        }
    }

    func delete(req: Request) throws -> EventLoopFuture<Response> {
        return Product.find(req.parameters.get("id"), on: req.db)
            .unwrap(or: Abort(.notFound))
            .flatMap { product in
                return product.delete(on: req.db).map {
                    req.redirect(to: "/products")
                }
            }
    }
}