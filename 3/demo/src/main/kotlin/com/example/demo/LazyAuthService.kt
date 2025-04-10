package com.example.demo

import jakarta.servlet.http.Cookie
import jakarta.servlet.http.HttpServletResponse
import jakarta.servlet.http.HttpServletRequest
import org.springframework.stereotype.Service
import org.springframework.context.annotation.Lazy

@Service
@Lazy
class LazyAuthService {

    init {
        System.out.println("LazyAuthService is loaded")
    }

    var authenticatedUsers: MutableSet<String> = mutableSetOf()
    fun authenticate(username: String, password: String): String? {
        if( username == "user" && password == "password") {
            val token = username.hashCode().toString()
            authenticatedUsers.add(token)
            return token
        }
        return null
    }
    fun checkToken(token: String): Boolean {
        return authenticatedUsers.contains(token)
    }
    fun tryAuthenticate(user: User, response: HttpServletResponse): String {
		val token = authenticate(user.username, user.password)
		return if (token != null) {
			val cookie = Cookie("token", token)
            cookie.path = "/"
            cookie.isHttpOnly = true
            response.addCookie(cookie)
            response.status = HttpServletResponse.SC_FOUND
            response.setHeader("Location", "/products")
            "Authenticated successfully"
		} else {
            response.status = HttpServletResponse.SC_FOUND
            response.setHeader("Location", "/login.html")
			"Authentication failed"
		}
	}
}    

