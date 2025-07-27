<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<style>
body{
  padding:0px;
  margin:0px;
  width: 100%;
  height: 100%;
  overflow: hidden;
}
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 0px;
  background-color: #01080d;
}
::-webkit-scrollbar {
  display: none;
}
</style>