<template>
  <div id="app">
    <img src="./assets/logo.png">
    <ClassListing/>
  </div>
</template>

<script>
import ClassListing from './components/ClassListing';

export default {
  name: 'App',
  components: {
    ClassListing,
  },
};
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
