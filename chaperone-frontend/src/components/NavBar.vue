<template>
    <div>
        <aside id="logo-sidebar" class="fixed top-0 left-0 z-40 w-72 h-screen transition-transform -translate-x-full sm:translate-x-0" aria-label="Sidebar">
            <div class="h-full px-3 py-4 overflow-y-auto bg-gray-200">
                <a href="https://flowbite.com/" class="flex items-center pl-2.5 mb-5">
                    <img src="https://flowbite.com/docs/images/logo.svg" class="h-6 mr-3 sm:h-7" alt="Flowbite Logo" />
                    <span class="self-center text-xl font-semibold whitespace-nowrap dark:text-white">Plend AI</span>
                </a>
  
                <ul class="space-y-2 font-medium">
                    <NavBarItem content-name="Opportunity" url="opportunity-list"></NavBarItem>
                    <NavBarItem content-name="Application" url="application-list"></NavBarItem>
                </ul>
  
            </div>
        </aside>
  
    </div>
  </template>
  
  <script>
  import NavBarItem from '../components/NavBarItem.vue'
  
  export default {
    components: {
      NavBarItem
    }
  }
  
  
  </script>