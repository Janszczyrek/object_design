import Fluent
import Vapor

func routes(_ app: Application) throws {
    let productController = ProductController()

    try app.register(collection: productController)
}