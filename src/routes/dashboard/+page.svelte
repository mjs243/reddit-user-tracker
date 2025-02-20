<script lang="ts">
  import { onMount } from 'svelte';
  
  // In a real app, these would come from your auth store.
  const currentUser = 'your_reddit_username';
  
  let trackedUsers: string[] = [];
  let newUser = '';

  // Fetch the list of tracked users from your backend.
  async function fetchTrackedUsers() {
    // Ensure your FastAPI backend has a GET endpoint (e.g., /tracked-users)
    // that returns an array of tracked usernames.
    const res = await fetch('http://localhost:8000/tracked-users', {
      headers: {
        'X-Reddit-Username': currentUser
      }
    });
    trackedUsers = await res.json();
  }

  // Function to add a tracked user.
  async function addUser() {
    const res = await fetch(`http://localhost:8000/track/${newUser}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Reddit-Username': currentUser
      }
    });
    const result = await res.json();
    console.log(result);
    await fetchTrackedUsers();
    newUser = '';
  }

  // Function to remove a tracked user.
  async function removeUser(username: string) {
    const res = await fetch(`http://localhost:8000/untrack/${username}`, {
      method: 'DELETE',
      headers: {
        'X-Reddit-Username': currentUser
      }
    });
    const result = await res.json();
    console.log(result);
    await fetchTrackedUsers();
  }

  onMount(() => {
    fetchTrackedUsers();
  });
</script>

<div class="container mx-auto p-4">
  <h1 class="text-2xl font-bold mb-4">Dashboard</h1>
  
  <!-- Form to add a tracked user -->
  <div class="mb-4">
    <input 
      type="text" 
      bind:value={newUser} 
      placeholder="Enter Reddit username" 
      class="border rounded p-2 mr-2" />
    <button 
      on:click={addUser} 
      class="bg-blue-500 text-white px-4 py-2 rounded">
      Track User
    </button>
  </div>
  
  <!-- List of tracked users -->
  <ul>
    {#each trackedUsers as user}
      <li class="flex justify-between items-center p-2 border-b">
        <span>{user}</span>
        <button 
          on:click={() => removeUser(user)} 
          class="bg-red-500 text-white px-2 py-1 rounded">
          Remove
        </button>
      </li>
    {/each}
  </ul>
</div>
