<template>
    <div>
      <!-- Hero Section -->
      <section class="pt-28 pb-20 md:py-32 bg-gradient-to-b from-white to-purple-50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div class="flex flex-col md:flex-row items-center">
            <div class="md:w-1/2 mb-12 md:mb-0">
              <h1 class="text-4xl md:text-5xl font-bold mb-6 leading-tight">
                Expand Your <span class="gradient-text">Vocabulary</span> While Managing Screen Time
              </h1>
              <p class="text-xl text-gray-600 mb-8">
                Chaperone is an AI-powered Chrome extension that helps you learn new words through fun games while promoting digital wellbeing.
              </p>
              <div class="flex flex-col sm:flex-row gap-4">
                <button @click="scrollToDownload" class="gradient-bg text-white px-6 py-3 rounded-lg hover:opacity-90 transition-opacity duration-300 flex items-center justify-center">
                  <i class="fas fa-download mr-2"></i> Get Started
                </button>
                <button @click="scrollToHowItWorks" class="bg-white text-purple-600 border border-purple-600 px-6 py-3 rounded-lg hover:bg-purple-50 transition-colors duration-300 flex items-center justify-center">
                  <i class="fas fa-play-circle mr-2"></i> How It Works
                </button>
              </div>
            </div>
            <div class="md:w-1/2 flex justify-center">
              <div class="relative">
                <div class="w-64 h-64 md:w-80 md:h-80 bg-purple-100 rounded-full absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2"></div>
                <img src="https://res.cloudinary.com/iyanuashiri/image/upload/v1746660880/app-screenshot_stkzvs.jpg" alt="Chaperone App Screenshot" class="floating relative z-10 rounded-2xl shadow-xl">
              </div>
            </div>
          </div>
        </div>
      </section>
  
      <!-- Stats Section -->
      <section class="py-16 bg-white">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div class="flex flex-col items-center p-6 bg-purple-50 rounded-xl">
              <div class="w-16 h-16 flex items-center justify-center bg-purple-100 rounded-full mb-4">
                <i class="fas fa-book text-purple-600 text-2xl"></i>
              </div>
              <h3 class="text-3xl font-bold mb-2">10,000+</h3>
              <p class="text-gray-600 text-center">Words in our database</p>
            </div>
            <div class="flex flex-col items-center p-6 bg-purple-50 rounded-xl">
              <div class="w-16 h-16 flex items-center justify-center bg-purple-100 rounded-full mb-4">
                <i class="fas fa-users text-purple-600 text-2xl"></i>
              </div>
              <h3 class="text-3xl font-bold mb-2">50,000+</h3>
              <p class="text-gray-600 text-center">Active users</p>
            </div>
            <div class="flex flex-col items-center p-6 bg-purple-50 rounded-xl">
              <div class="w-16 h-16 flex items-center justify-center bg-purple-100 rounded-full mb-4">
                <i class="fas fa-clock text-purple-600 text-2xl"></i>
              </div>
              <h3 class="text-3xl font-bold mb-2">30%</h3>
              <p class="text-gray-600 text-center">Average reduction in social media usage</p>
            </div>
          </div>
        </div>
      </section>
  
      <!-- Features Section -->
      <section id="features" class="py-20 bg-gray-50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div class="text-center mb-16">
            <h2 class="text-3xl md:text-4xl font-bold mb-4">Why Choose Chaperone?</h2>
            <p class="text-xl text-gray-600 max-w-3xl mx-auto">Our unique approach combines vocabulary improvement with digital wellbeing tools to help you grow while maintaining balance.</p>
          </div>
          
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            <div v-for="(feature, index) in features" :key="`feature-${index}`" class="bg-white p-6 rounded-xl shadow-sm hover:shadow-md transition-shadow duration-300">
              <div class="w-12 h-12 flex items-center justify-center bg-purple-100 rounded-full mb-4">
                <i :class="`fas ${feature.icon} text-purple-600`"></i>
              </div>
              <h3 class="text-xl font-semibold mb-3">{{ feature.title }}</h3>
              <p class="text-gray-600">{{ feature.description }}</p>
            </div>
          </div>
        </div>
      </section>
  
      <!-- How It Works Section -->
      <section id="how-it-works" class="py-20 bg-white">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div class="text-center mb-16">
            <h2 class="text-3xl md:text-4xl font-bold mb-4">How Chaperone Works</h2>
            <p class="text-xl text-gray-600 max-w-3xl mx-auto">Our simple yet powerful approach transforms your browsing experience into learning opportunities.</p>
          </div>
          
          <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div v-for="(step, index) in howItWorks" :key="`step-${index}`" class="flex flex-col items-center text-center">
              <div class="w-16 h-16 flex items-center justify-center bg-purple-100 rounded-full mb-4">
                <span class="text-purple-600 font-bold text-xl">{{ index + 1 }}</span>
              </div>
              <h3 class="text-xl font-semibold mb-3">{{ step.title }}</h3>
              <p class="text-gray-600">{{ step.description }}</p>
              <img :src="step.image" :alt="`${step.title} Step`" class="mt-6 rounded-lg shadow-md">
            </div>
          </div>
        </div>
      </section>
  
      <!-- Game Showcase Section -->
      <section class="py-20 bg-purple-50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div class="text-center mb-16">
            <h2 class="text-3xl md:text-4xl font-bold mb-4">Fun Vocabulary Games</h2>
            <p class="text-xl text-gray-600 max-w-3xl mx-auto">Our games make learning new words enjoyable and effective.</p>
          </div>
          
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div v-for="(game, index) in games" :key="`game-${index}`" class="bg-white p-4 rounded-xl shadow-sm hover:shadow-md transition-shadow duration-300">
              <img :src="game.image" :alt="`${game.title} Game`" class="w-full h-40 object-cover rounded-lg mb-4">
              <h3 class="text-lg font-semibold mb-2">{{ game.title }}</h3>
              <p class="text-gray-600 text-sm">{{ game.description }}</p>
            </div>
          </div>
        </div>
      </section>
  
      <!-- Testimonials Section -->
      <section id="testimonials" class="py-20 bg-white">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div class="text-center mb-16">
            <h2 class="text-3xl md:text-4xl font-bold mb-4">What Our Users Say</h2>
            <p class="text-xl text-gray-600 max-w-3xl mx-auto">Join thousands of satisfied users who have improved their vocabulary while reducing screen time.</p>
          </div>
          
          <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div v-for="(testimonial, index) in testimonials" :key="`testimonial-${index}`" class="bg-gray-50 p-6 rounded-xl shadow-sm">
              <div class="flex items-center mb-4">
                <div class="flex-shrink-0">
                  <img :src="testimonial.avatar" alt="User Avatar" class="w-12 h-12 rounded-full">
                </div>
                <div class="ml-4">
                  <h4 class="font-semibold">{{ testimonial.name }}</h4>
                  <div class="flex text-yellow-400">
                    <i v-for="star in 5" :key="`star-${star}`" :class="star <= testimonial.rating ? 'fas fa-star' : star - 0.5 === testimonial.rating ? 'fas fa-star-half-alt' : 'far fa-star'"></i>
                  </div>
                </div>
              </div>
              <p class="text-gray-600">{{ testimonial.quote }}</p>
            </div>
          </div>
        </div>
      </section>
  
      <!-- CTA Section -->
      <section id="download" class="py-20 gradient-bg">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 class="text-3xl md:text-4xl font-bold mb-6 text-white">Ready to Transform Your Browsing Experience?</h2>
          <!-- <p class="text-xl text-white opacity-90 max-w-3xl mx-auto mb-10">Download Chaperone today and start building your vocabulary while improving your digital wellbeing.</p> -->
          
          <p class="text-xl text-white opacity-90 max-w-3xl mx-auto mb-10">Be first to experience Chaperone by joining the waitlist now to get early access and shape the future of mindful tech.</p>

          <div class="flex flex-col sm:flex-row justify-center gap-6">
            <a href="https://docs.google.com/forms/d/e/1FAIpQLScvq89bz1m1U6skCWIWmn-spot7xKGvNpqW8dEv8I0hV8-uzw/viewform?usp=header" class="bg-white text-purple-600 px-8 py-4 rounded-lg hover:bg-gray-100 transition-colors duration-300 flex items-center justify-center">
              <i class="fab fa-chrome text-2xl mr-3"></i>
              <div class="text-left">
                <div class="text-sm">Join the waitlist now</div>
                <!-- <div class="font-semibold">Chrome</div> -->
              </div>
            </a>

            <!-- <a href="#" class="bg-white text-purple-600 px-8 py-4 rounded-lg hover:bg-gray-100 transition-colors duration-300 flex items-center justify-center">
              <i class="fab fa-chrome text-2xl mr-3"></i>
              <div class="text-left">
                <div class="text-sm">Add to</div>
                <div class="font-semibold">Chrome</div>
              </div>
            </a> -->
            
            <!-- <a href="#" class="bg-white text-purple-600 px-8 py-4 rounded-lg hover:bg-gray-100 transition-colors duration-300 flex items-center justify-center">
              <i class="fas fa-globe text-2xl mr-3"></i>
              <div class="text-left">
                <div class="text-sm">Use</div>
                <div class="font-semibold">Web App</div>
              </div>
            </a> -->
          </div>
        </div>
      </section>
    </div>
  </template>
  
  <script>
  export default {
    name: 'HomePage',
    data() {
      return {
        features: [
          {
            icon: 'fa-gamepad',
            title: 'Gamified Learning',
            description: 'Expand your vocabulary through fun interactive games that make learning enjoyable and effective.'
          },
          {
            icon: 'fa-brain',
            title: 'AI-Powered',
            description: 'Our AI adapts to your learning style and vocabulary level to provide personalized word suggestions.'
          },
          {
            icon: 'fa-chart-line',
            title: 'Progress Tracking',
            description: 'Visualize your learning journey with detailed statistics and progress reports.'
          },
          {
            icon: 'fa-hourglass-half',
            title: 'Screen Time Management',
            description: 'Set healthy limits on social media and distracting websites while replacing that time with learning.'
          },
          {
            icon: 'fa-bell',
            title: 'Smart Notifications',
            description: 'Receive gentle reminders to take breaks and engage with vocabulary games during your browsing.'
          },
          {
            icon: 'fa-sync-alt',
            title: 'Sync Across Devices',
            description: 'Access your vocabulary lists and progress on both the web app and Chrome extension.'
          }
        ],
        howItWorks: [
          {
            title: 'Install & Setup',
            description: 'Download the Chrome extension, create an account, and set your vocabulary level and screen time goals.',
            // image: '/images/step-1.png'
            image: 'https://res.cloudinary.com/iyanuashiri/image/upload/v1746660880/step-1_qhvdeb.jpg'
          },
          {
            title: 'Browse & Learn',
            description: 'As you browse, Chaperone monitors your time and suggests short vocabulary games during breaks.',
            image: 'https://res.cloudinary.com/iyanuashiri/image/upload/v1746660880/step-2_rgmjoh.jpg'
          },
          {
            title: 'Track & Improve',
            description: 'Review your progress, earn rewards for consistency, and watch your vocabulary expand while digital habits improve.',
            image: 'https://res.cloudinary.com/iyanuashiri/image/upload/v1746660879/step-3_cgdmol.jpg'
          }
        ],
        games: [
          {
            title: 'Word Match',
            description: 'Match words with their definitions against the clock.',
            image: 'https://res.cloudinary.com/iyanuashiri/image/upload/v1746660879/game-synonym_pbqrgx.jpg'
          },
          {
            title: 'Sentence Fill',
            description: 'Complete sentences with the most appropriate word.',
            image: 'https://res.cloudinary.com/iyanuashiri/image/upload/v1746660879/game-synonym_pbqrgx.jpg'
          },
          {
            title: 'Word Builder',
            description: 'Create as many words as possible from given letters.',
            image: 'https://res.cloudinary.com/iyanuashiri/image/upload/v1746660879/game-synonym_pbqrgx.jpg'
          },
          {
            title: 'Synonym Challenge',
            description: 'Identify synonyms and antonyms to expand your word associations.',
            image: 'https://res.cloudinary.com/iyanuashiri/image/upload/v1746660879/game-synonym_pbqrgx.jpg'
          }
        ],
        testimonials: [
          {
            name: 'Sarah L.',
            avatar: 'https://res.cloudinary.com/iyanuashiri/image/upload/v1746660879/avatar-1_q0p8sd.jpg',
            rating: 5,
            quote: '"Chaperone has completely changed how I use my browser. I\'ve cut my social media time in half and learned over 200 new words in just 3 months!"'
          },
          {
            name: 'Michael T.',
            avatar: 'https://res.cloudinary.com/iyanuashiri/image/upload/v1746660879/avatar-2_ferkv3.jpg',
            rating: 4.5,
            quote: '"As a writer, I\'m always looking to expand my vocabulary. The games are addictive and I find myself choosing them over mindless scrolling!"'
          },
          {
            name: 'Jamie K.',
            avatar: 'https://res.cloudinary.com/iyanuashiri/image/upload/v1746660879/avatar-3_hyv9ur.jpg',
            rating: 5,
            quote: '"I installed Chaperone to help with my English studies, but the digital wellbeing features have been an unexpected bonus. My screen time report has never looked better!"'
          }
        ]
      };
    },
    methods: {
      scrollToDownload() {
        document.getElementById('download').scrollIntoView({ behavior: 'smooth' });
      },
      scrollToHowItWorks() {
        document.getElementById('how-it-works').scrollIntoView({ behavior: 'smooth' });
      }
    }
  };
  </script>
  
  <style scoped>
  @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
  
  .gradient-text {
    background: linear-gradient(90deg, #7C3AED, #4F46E5);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }
  
  .gradient-bg {
    background: linear-gradient(90deg, #7C3AED, #4F46E5);
  }
  
  .floating {
    animation: float 3s ease-in-out infinite;
  }
  
  @keyframes float {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-20px); }
    100% { transform: translateY(0px); }
  }
  </style>