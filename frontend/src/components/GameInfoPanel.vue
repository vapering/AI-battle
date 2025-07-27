<template>
  <v-container fluid class="game-info-panel">
    <!-- 主要内容区域 - 响应式双列布局 -->
    <v-row class="gap-4">
      <v-col cols="12" class="game-command-history-parent-container ">
          <!-- 玩家信息 -->
          <div class="game-command-history-parent panel-bg-player">
            <div v-for="player in sortedPlayers" :style="{ backgroundColor: player.background_color }" :key="player.id" class="faction-item rounded" :class="{ 'defeated-row': player.is_defeated }">
              <div class="player-info-basic"> 
                <span class="player-name font-weight-bold">{{ player.name }}</span>
                <span>| {{ player.model || 0 }}</span>
                <span class="player-status px-2 py-1 rounded text-xs" :class="player.is_defeated ? 'bg-red-100 text-red-800' : 'bg-green-100 text-green-800'">{{ player.is_defeated ? '失败' : '存活' }}</span>
                <template v-if="player.is_defeated"> (存活: {{ player.alive_turns }}回合)</template>
              </div>
              <div class="player-info-basic">
                <span class="player-city">|州: {{ player.city_count || 0 }}</span>
                <span class="player-troops">|兵力: {{ formatTroops(player.total_troops || 0) }}</span>
                <span class="player-command-success">|指令成功率: {{ player.total_commands > 0 ? (player.successful_commands / player.total_commands * 100).toFixed(1) + '%' : '0%' }} | 指令总数：{{ player.total_commands }}</span>
              </div>
            </div>
          </div>

        <!-- 指令历史记录 -->
        <div ref="commandHistory" class="game-command-history-parent panel-bg1">
          <div class="game-command-history">
            <div v-for="(cmd, index) in command_history.slice(-9)" :key="index" class="command-item">
              <span class="command-turn">{{ cmd.turn }}:  </span>
              <span class="command-player">{{ cmd.player_name }}</span>
              <span class="command-result">{{ cmd.result }}</span>
              <span class="command-content">{{ cmd.command }}</span>
            </div>
          </div>
        </div>

        <!-- 游戏事件 -->
        <div ref="gameEventsRef" class="game-command-history-parent panel-bg2">
          <div class="game-command-history">
            <div v-for="(event, index) in game_events.slice(-9)" :key="index" class="command-item">
              <span class="command-turn">{{ event.turn }}:  </span>
              <span class="command-player">{{ event.player_id }}</span>
              <span class="command-content">{{ event.content }}</span>
            </div>
          </div>
        </div>
      </v-col>
    </v-row>
  </v-container>
  <!-- 玩家台词 -->
  <div ref="commentary" class="game-commentary-parent-container">
    <div class="panel-bg3 game-commentary-parent">
      <div v-for="(line, index) in (global_lines || []).slice(-5)" :key="index" class="player-line-item">
        {{ line }}
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'GameInfoPanel',
  props: {
    gameDate: String,
    stateInfo: Array,
    players: Array,
    command_history: Array,
    game_events: Array,
    global_lines: Array,
  },
  computed: {
    sortedPlayers() {
      // 保持与原组件相同的排序逻辑
      return [...this.players].sort((a, b) => b.total_troops - a.total_troops);
    }
  },
  methods: {
    formatTroops(troops) {
      if (troops >= 10000) {
        return (troops / 10000).toFixed(1) + '万';
      }
      return troops.toString();
    },
    scrollToBottom() {
      this.$nextTick(() => {
        const element = this.$refs.commandHistory;
        if (element) {
          element.scrollTop = element.scrollHeight;
        }
      });
    }
  },
  watch: {
    // command_history() {
    //   this.scrollToBottom();
    // }
  }
}
</script>

<style scoped>
/* 导入Vuetify工具类 */
@import 'vuetify/styles';

.game-info-panel {
  /* background-color: #000000; */
  color:#CCCCFF;
  z-index: 10;
}

.faction-item {
  padding: 3px;
  margin:3px 0px;
  border-radius: 4px;
  color:#DDFFFF;
  transition: transform 0.2s;
  text-align: left;
}

.faction-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.defeated-row {
  opacity: 0.7;
  filter: grayscale(0);
}

.command-item {
  display: flex;
  justify-content: left;
  text-align: center;
  flex-wrap: wrap;
  margin: 0px;
  padding: 0px;
  font-family: 'AlibabaPuHuiTi-3-35-Thin, SimSun, Arial, sans-serif';
  font-size:12px;
}

.command-turn {
  flex:2;
  margin: 0px;
}

.command-player {
  flex:2;
  margin: 0px;
}
.command-result {
  flex: 2;
  white-space: nowrap;
}
.command-content {
  flex: 12;
  margin: 0px;
}

.player-info-basic {
  justify-content: left;
}
.game-command-history-parent-container{
  margin: 10px 0px;
  padding: 0px !important;
  position: relative;
  left: -100px;
  top: 0px;
  perspective: 1000px; /* 设置透视距离 */
  background-size: 100% 100%;
  background-position: center;
  overflow: visible;
}
.panel-bg-player{
  background: url('../assets/images/game-panel-player-1.png');
  padding-left: 200px !important;
  padding-right: 80px !important;
  font-size:13px !important;
  min-height: 200px;
  animation: game-bg-animate 300s infinite ease-in-out;
}
@keyframes game-bg-animate {
  0% {
    transform: translateX(30px) rotateY(-20deg);
  }
  50% {
    transform: translateX(60px) rotateY(-30deg);
  }
  100% {
    transform: translateX(30px) rotateY(-20deg);
  }
}
.panel-bg1{
  background: url('../assets/images/game-panel-1-1.png');
  animation: panel-bg1-animate 360s infinite ease-in-out;
}
.panel-bg2{
  background: url('../assets/images/game-panel-2-1.png');
  animation: panel-bg1-animate 260s infinite ease-in-out;
}
.panel-bg3{
  background: url('../assets/images/game-panel-3-1.png');
}
@keyframes panel-bg1-animate {
  0% {
    transform: translateX(30px) rotateY(-20deg);
  }
  50% {
    transform: translateX(60px) rotateY(-30deg);
  }
  100% {
    transform: translateX(30px) rotateY(-20deg);
  }
}
.game-command-history-parent{
  /* background: url('../assets/images/game-panel.png'); */
  background-size: 100% 100%;
  transform-style: preserve-3d; /* 保持3D变换 */
  transition: transform 2s; /* 平滑过渡效果 */
  transform: translateX(60px) rotateY(-30deg);
  background-position: center;
  background-repeat: no-repeat;
  font-size: 10px;
  padding: 36px 55px;
  overflow: hidden;
  margin: 20px 0px;
}
.game-command-history-parent:hover{
  transition: transform 1s; /* 平滑过渡效果 */
  transform: translateX(0px) rotateY(-5deg);
}

.game-command-history {
  height: 180px;
  overflow: hidden;
  border-radius: 4px;
}
.player-name{
  flex:4;
  text-align: left;
  font-size: 18px;
}
.player-status {
  flex:2;
}
.player-troops {
  text-align: left;
  flex:3;
  display: inline-flex;
  /* font-weight: bold; */
  /* color: #666; */
}
.player-slogan{
  font-size: 12px;
  text-align: left;
  flex:3;
  display: inline-flex;
}
.player-city {
  flex:2;
  display: inline-flex;
  /* font-weight: bold; */
  /* color: #666; */
}
.player-model {
  text-align: left;
  display: inline-flex;
  /* font-weight: bold; */
  /* color: #666; */
}
.game-commentary-parent-container{
  perspective: 1000px; /* 设置透视距离 */
  position: absolute !important;
  left: 10px;
  bottom: 90px;
  font-size: 12px;
}
.game-commentary-parent{
  background-size: 100% 100%;
  color:#CCCCFF;
  transform-style: preserve-3d;
  transition: transform 2s; 
  transform: translateY(60px) rotateX(30deg);
  padding: 50px 60px;
  width:560px;

  animation: game-commentary-animate 200s infinite ease-in-out;
}
.game-commentary-parent:hover{
  transform-style: preserve-3d; /* 保持3D变换 */
  transition: transform 1s; /* 平滑过渡效果 */
  transform: translateY(0px) rotateX(10deg);
}
.player-line-item{  
  text-align: left;
}

@keyframes game-commentary-animate {
  0% {
    transform: translateY(60px) rotateX(30deg);
  }
  50% {
    transform: translateY(30px) rotateX(25deg);
  }
  100% {
    transform: translateY(60px) rotateX(30deg);
  }
}

</style>