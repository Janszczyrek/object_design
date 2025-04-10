package com.example.demo

import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.boot.runApplication
import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.PostMapping
import org.springframework.web.bind.annotation.RequestBody
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RequestParam
import org.springframework.web.bind.annotation.RestController
import org.springframework.web.bind.annotation.CookieValue
import jakarta.servlet.http.Cookie
import jakarta.servlet.http.HttpServletResponse
import jakarta.servlet.http.HttpServletRequest
import org.springframework.beans.factory.annotation.Autowired

@SpringBootApplication
class DemoApplication

fun main(args: Array<String>) {
	runApplication<DemoApplication>(*args)
}


@RestController
class ProductController @Autowired constructor(private val authService: AuthService) {
	private val products = listOf(
		Product(1, "Product 1", "Description 1", 10.0),
		Product(2, "Product 2", "Description 2", 20.0),
		Product(3, "Product 3", "Description 3", 30.0)
	)

    @GetMapping("/products")
    fun getProducts(@CookieValue("token") token: String?, response: HttpServletResponse): List<Product> {
		if (token != null && authService.checkToken(token)) {
			System.out.println("Token is valid")
			return products
		}
		response.status = HttpServletResponse.SC_FOUND
		response.setHeader("Location", "/login.html")
		return emptyList()
    }
	@PostMapping("/auth")
	fun tryAuthenticate(@RequestParam("username") username: String, @RequestParam("password") password: String, response: HttpServletResponse): String {
		if (username.isEmpty() || password.isEmpty()) {
			return "Username and password cannot be empty"
		}
		val user = User(username, password)
		return authService.tryAuthenticate(user, response)
	}

}
