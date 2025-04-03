package com.example.demo

import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.boot.runApplication
import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RestController

@SpringBootApplication
class DemoApplication

fun main(args: Array<String>) {
	runApplication<DemoApplication>(*args)
}

data class Product(
	val id: Long,
	val name: String,
	val description: String,
	val price: Double
)

@RestController
class ProductController {
	private val products = listOf(
		Product(1, "Product 1", "Description 1", 10.0),
		Product(2, "Product 2", "Description 2", 20.0),
		Product(3, "Product 3", "Description 3", 30.0)
	)

    @GetMapping("/product")
    fun sayHello(): List<Product> {
        return products
    }

}
