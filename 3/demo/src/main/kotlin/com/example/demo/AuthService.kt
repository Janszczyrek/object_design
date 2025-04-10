import jakarta.servlet.http.Cookie
import jakarta.servlet.http.HttpServletResponse
import jakarta.servlet.http.HttpServletRequest
import User

object AuthService {
    var authenticatedUsers: MutableSet<String> = mutableSetOf()
    fun authenticate(username: String, password: String): String? {
        // Simulate authentication logic
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
		val token = AuthService.authenticate(user.username, user.password)
		return if (token != null) {
			val cookie = Cookie("token", token)
            cookie.path = "/"
            cookie.isHttpOnly = true
            response.addCookie(cookie)
            "Authentication successful"
		} else {
			"Authentication failed"
		}
	}
}    

