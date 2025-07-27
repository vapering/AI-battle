<template>
  <span class="game-progress">
    <span>
      {{ currentTurn }} 回合, {{ stateCount }}个州
    </span>
    <button @click="handleStartGame" class="start-game-btn">游戏开始</button>
    <button @click="handleContinueGame" class="start-game-btn">继续游戏</button>
    <button @click="handlePauseGame" class="start-game-btn">暂停游戏</button>
    <button @click="handleLoadGame" class="start-game-btn">从存档处继续</button>
  </span>
</template>

<script>
export default {
  name: 'GameControls',
  props: {
    currentTurn: {
      type: Number,
      default: 0
    },
    stateCount: {
      type: Number,
      default: 0
    }
  },
  methods: {
    handleStartGame() {
      this.$emit('start-game');
    },
    handleContinueGame() {
      this.$emit('continue-game');
    },
    handlePauseGame() {
      this.$emit('pause-game');
    },
    handleLoadGame() {
      this.$emit('load-game');
    }
  }
}
</script>

<style scoped>
/* 保持原有样式不变 */
.game-progress {
  gap: 10px;
  padding: 15px;
  justify-content: center;
  color: #CCCCFF;
  z-index: 10;
}
.start-game-btn {
  padding: 8px 16px;
  background-image: url('../assets/images/game-btn.png');
  background-size: 100% 100%;
  cursor: pointer;
  font-size: 14px;
  color: #9999FF;
  transition: background-color 0.3s;
}
.start-game-btn:hover {
  color: #CCCCFF;
  margin-bottom: 3px;
}

</style>