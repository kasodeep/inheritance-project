import { Nav } from './components'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Home from './pages/Home'
import About from './pages/About'
import Login from './pages/Login'
import Signup from './pages/Signup'

function App() {
  return (
    // React Router Setup
    <Router>
      {/* Navbar */}
      <Nav />
      <Routes>
        {/* Home */}
        <Route path="/" element={<Home />} />

        {/* About */}
        <Route path="/about" element={<About />} />

        {/* Login */}
        <Route path="/login" element={<Login />} />

        {/* Sign Up */}
        <Route path="/signup" element={<Signup />} />

        {/* Error Page */}
        <Route path="*" element={<h2>Page Not Found</h2>} />
      </Routes>
    </Router>
  )
}

export default App
