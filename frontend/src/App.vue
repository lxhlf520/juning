<template>
  <NavBar />
  <main>
    <HeroSection />
    <ServicesSection />
    <CasesSection />
    <AboutSection />
    <ContactSection />
  </main>
  <FooterSection />
</template>

<script setup lang="ts">
import { useScrollReveal } from '@/composables/useScrollReveal'
import NavBar from '@/components/NavBar.vue'
import HeroSection from '@/components/HeroSection.vue'
import ServicesSection from '@/components/ServicesSection.vue'
import CasesSection from '@/components/CasesSection.vue'
import AboutSection from '@/components/AboutSection.vue'
import ContactSection from '@/components/ContactSection.vue'
import FooterSection from '@/components/FooterSection.vue'

useScrollReveal()
</script>
