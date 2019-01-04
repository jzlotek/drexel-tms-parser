<template>
  <v-app dark id="app">
    <ClassSearch/>
    <ClassListing/>
    <v-alert
      :value="alert"
      type="error"
      transition="scale-transition"
    >
      {{ alertData }}
    </v-alert>
  </v-app>
</template>

<script>
import ClassListing from './components/ClassListing';
import ClassSearch from './components/ClassSearch';
import EventBus from './EventBus';

export default {
  name: 'App',
  components: {
    ClassListing,
    ClassSearch,
  },
  data() {
    return {
      alert: false,
      alertData: null,
    };
  },
  mounted() {
    EventBus.$on('error', (data) => {
      this.alert = true;
      this.alertData = data;
      setTimeout(() => { this.alert = false; }, 5000);
    });
  },
};
</script>

<style>

</style>
