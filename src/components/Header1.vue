<template>
   <v-app id="Header1">
      <v-navigation-drawer
              v-model="drawer"
              absolute
              temporary
              style="z-index: 5001"
      >
         <v-list dense>
            <v-list-tile ripple @click="">
               <v-list-tile-action>
                  <v-icon color="teal">map</v-icon>
               </v-list-tile-action>
               <v-list-tile-content>
                  <v-list-tile-title>Map</v-list-tile-title>
               </v-list-tile-content>
            </v-list-tile>
            <v-list-tile ripple @click="">
               <v-list-tile-action>
                  <v-icon color="purple">dashboard</v-icon>
               </v-list-tile-action>
               <v-list-tile-content>
                  <v-list-tile-title>Dashboard</v-list-tile-title>
               </v-list-tile-content>
            </v-list-tile>
            <v-list-tile ripple @click="">
               <v-list-tile-action>
                  <v-icon color="orange">table_chart</v-icon>
               </v-list-tile-action>
               <v-list-tile-content>
                  <v-list-tile-title>Tabular</v-list-tile-title>
               </v-list-tile-content>
            </v-list-tile>
            <v-list-tile ripple @click="">
               <v-list-tile-action>
                  <v-icon color="blue">bar_chart</v-icon>
               </v-list-tile-action>
               <v-list-tile-content>
                  <v-list-tile-title>Analytics</v-list-tile-title>
               </v-list-tile-content>
            </v-list-tile>
            <v-list-tile ripple @click="">
               <v-list-tile-action>
                  <v-icon color="#ff0000">category</v-icon>
               </v-list-tile-action>
               <v-list-tile-content>
                  <v-list-tile-title>Thematics</v-list-tile-title>
               </v-list-tile-content>
            </v-list-tile>
         </v-list>
      </v-navigation-drawer>
      <v-toolbar color="primary" dark absolute app style="z-index:5000">
         <v-toolbar-side-icon @click.stop="drawer = !drawer"></v-toolbar-side-icon>
         <span class="logoContainer">
            <img src="https://agw-prim-green2.csr.utexas.edu/images/moves.png" class="logoImageMediaSensitive" alt="MOVES Logo"></img>
         </span>

         <!-- <MenuScreenTools app />
        <MenuMainTools app />
         <MenuSecondaryTools app />-->


      </v-toolbar>
      <v-content>
         <v-container fluid fill-height style="margin:0">

            <Map />

         </v-container>
      </v-content>
   </v-app>
</template>

<script>
   import Map from './Map.vue';

   export default {
      name:"Header1",
      components: {
         //MenuMainTools,
         //MenuSecondaryTools,
         //MenuScreenTools,
         Map
         //Footer1
      },
      created() {
         this.$eventHub.$on('logged-in', this.getCurrentUser)
      },
      data: () => ({
         drawer: null
      }),
      props: {
         source: String
      }
   }
</script>
<style>
   .container{
      padding:0;
   }
   .v-navigation-drawer--temporary{
      z-index:5000;
   }
   .logoImageMediaSensitive{
      max-width: 100%;
      width: 100%;
      height: auto !important;
   }
   .logoContainer{
      width:144px;
      height:44px;
   }
   .v-speed-dial{
      z-index:5000;
   }
   @media (max-width:480px) {
      .logoContainer{
         max-width: 72px;
         max-height: 22px;
      }
      .logoImageMediaSensitive {
         max-width: 72px;
         max-height: 22px;
      }
      .headerToolbar{
         z-index:5000;
      }
   }
</style>