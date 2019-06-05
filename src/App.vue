<template>
  <div id="app">
    <Header1/>
    <SensorChoices/>
  </div>
</template>

<script>
  //import Hello from './components/Hello.vue';
  import Header1 from './components/Header1.vue';
  //import SensorChoices from './components/SensorChoices.vue';
  import store from 'store';

  export default {
    name: 'App',
    components: {
      Header1
      //SensorChoices
    }
  }

  //store.commit('increment');
  //console.log(store.getters.evenOrOdd);
  //store.commit('increment');
  //console.log(store.getters.evenOrOdd);
  //console.log(store.state.count);
</script>

<style>
  #app {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    margin-top: 0;
  }
</style>