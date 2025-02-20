<script lang="ts">
  function login() {
    // Redirect to your FastAPI backend's login endpoint.
    window.location.href = 'http://localhost:8000/auth/login';
  }
</script>

<div class="container mx-auto p-4">
  <h1 class="text-2xl font-bold mb-4">Login</h1>
  <button 
    on:click={login} 
    class="bg-green-500 text-white px-4 py-2 rounded">
    Login with Reddit
  </button>
</div>
