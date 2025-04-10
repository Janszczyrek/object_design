package com.example.demo

import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.PostMapping
import org.springframework.web.bind.annotation.RequestParam
import org.springframework.web.bind.annotation.RestController
import org.springframework.web.bind.annotation.CookieValue
import jakarta.servlet.http.HttpServletResponse
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.context.annotation.Lazy

@RestController
class LazyAuthController @Autowired constructor(@Lazy private val lazyAuthService: LazyAuthService) {
    
    @GetMapping("/lazy-check")
    fun check(): String {
        lazyAuthService.checkToken("some-token")
        return "LazyAuthService is loaded"
    }
}