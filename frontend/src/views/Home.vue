<template>

  <v-container fluid class="pa-0 fill-height">
    <v-row no-gutters class="fill-height">
      <v-col cols="12" class="game-title">
        <!-- 游戏控制面板 -->
        <GameControls
          :current-turn="currentTurn"
          :state-count="stateInfo.length"
          @start-game="startGame"
          @continue-game="continueGame"
          @pause-game="pauseGame"
          @load-game="loadGame"
        />
      </v-col>
      <!-- 主地图区域预占用位置 -->
      <v-col cols="8" class="relative fill-height">
        <div id="map-container" class="inset-0 clear-both">
          <div id="mapSvg0" class="map-svg" style="z-index: 0;"></div>
        </div>
      </v-col>

      <!-- 侧边信息面板 -->
      <v-col cols="4">
        <v-row no-gutters>
          <v-col cols="12">

          </v-col>
          <v-col cols="12">
            <!-- 游戏信息面板 -->
            <GameInfoPanel 
              :game_events="game_events"
              :game-date="gameDate"
              :state-info="stateInfo"
              :players="players"
              :command_history="command_history"
              :global_lines="global_lines"
            />
          </v-col>
        </v-row>
      </v-col>
    </v-row>

    <!-- 游戏解说区域 -->
    <!-- <v-card elevation="2" class="mt-2">
      <v-card-text class="game-commentary pa-4">
        {{ commentaryResult }}
      </v-card-text>
    </v-card> -->
  </v-container>
</template>

<script>
import GameControls from '@/components/GameControls.vue';
import GameInfoPanel from '@/components/GameInfoPanel.vue';

export default {
  components: {
    GameControls,
    GameInfoPanel
  },

  name: 'AmericanCivilWar',
  data() {
    return {
      // SVG命名空间常量
      // 集中配置对象
      config: {
        SVG_NAMESPACE: 'http://www.w3.org/2000/svg',
        svgFilePath: require('@/assets/images/us.svg'),
        mapContainerSelector: '.map-svg',
        textStyle: {
          fontFamily: 'AlibabaPuHuiTi-3-35-Thin, SimSun, Arial, sans-serif',
          fontWeight: 'lighter',
          fontSize: '9px',
          color: '#b3fff5'
        },
        colorConfig: {
          saturationRange: [30, 70],
          lightnessRange: [40, 80]
        },
        no_owner_color: "#666",
      },
      roads: [{ "city_1": "华盛顿", "city_2": "爱达荷" }, { "city_1": "华盛顿", "city_2": "俄勒冈" }, { "city_1": "俄勒冈", "city_2": "爱达荷" }, { "city_1": "俄勒冈", "city_2": "内华达" }, { "city_1": "俄勒冈", "city_2": "加利福尼亚" }, { "city_1": "爱达荷", "city_2": "蒙大拿" }, { "city_1": "爱达荷", "city_2": "怀俄明" }, { "city_1": "爱达荷", "city_2": "犹他" }, { "city_1": "爱达荷", "city_2": "内华达" }, { "city_1": "蒙大拿", "city_2": "北达科他" }, { "city_1": "蒙大拿", "city_2": "南达科他" }, { "city_1": "蒙大拿", "city_2": "怀俄明" }, { "city_1": "北达科他", "city_2": "南达科他" }, { "city_1": "北达科他", "city_2": "明尼苏达" }, { "city_1": "南达科他", "city_2": "怀俄明" }, { "city_1": "南达科他", "city_2": "内布拉斯加" }, { "city_1": "南达科他", "city_2": "艾奥瓦" }, { "city_1": "南达科他", "city_2": "明尼苏达" }, { "city_1": "怀俄明", "city_2": "内布拉斯加" }, { "city_1": "怀俄明", "city_2": "科罗拉多" }, { "city_1": "怀俄明", "city_2": "犹他" }, { "city_1": "内布拉斯加", "city_2": "科罗拉多" }, { "city_1": "内布拉斯加", "city_2": "堪萨斯" }, { "city_1": "内布拉斯加", "city_2": "密苏里" }, { "city_1": "内布拉斯加", "city_2": "艾奥瓦" }, { "city_1": "科罗拉多", "city_2": "新墨西哥" }, { "city_1": "科罗拉多", "city_2": "堪萨斯" }, { "city_1": "科罗拉多", "city_2": "俄克拉荷马" }, { "city_1": "科罗拉多", "city_2": "犹他" }, { "city_1": "犹他", "city_2": "内华达" }, { "city_1": "犹他", "city_2": "亚利桑那" }, { "city_1": "内华达", "city_2": "亚利桑那" }, { "city_1": "内华达", "city_2": "加利福尼亚" }, { "city_1": "加利福尼亚", "city_2": "亚利桑那" }, { "city_1": "亚利桑那", "city_2": "新墨西哥" }, { "city_1": "新墨西哥", "city_2": "俄克拉荷马" }, { "city_1": "新墨西哥", "city_2": "得克萨斯" }, { "city_1": "得克萨斯", "city_2": "俄克拉荷马" }, { "city_1": "得克萨斯", "city_2": "阿肯色" }, { "city_1": "得克萨斯", "city_2": "路易斯安那" }, { "city_1": "俄克拉荷马", "city_2": "堪萨斯" }, { "city_1": "俄克拉荷马", "city_2": "密苏里" }, { "city_1": "俄克拉荷马", "city_2": "阿肯色" }, { "city_1": "堪萨斯", "city_2": "密苏里" }, { "city_1": "密苏里", "city_2": "艾奥瓦" }, { "city_1": "密苏里", "city_2": "伊利诺伊" }, { "city_1": "密苏里", "city_2": "肯塔基" }, { "city_1": "密苏里", "city_2": "田纳西" }, { "city_1": "密苏里", "city_2": "阿肯色" }, { "city_1": "艾奥瓦", "city_2": "明尼苏达" }, { "city_1": "艾奥瓦", "city_2": "威斯康星" }, { "city_1": "艾奥瓦", "city_2": "伊利诺伊" }, { "city_1": "明尼苏达", "city_2": "威斯康星" }, { "city_1": "威斯康星", "city_2": "密歇根" }, { "city_1": "威斯康星", "city_2": "伊利诺伊" }, { "city_1": "密歇根", "city_2": "印第安纳" }, { "city_1": "密歇根", "city_2": "俄亥俄" }, { "city_1": "伊利诺伊", "city_2": "印第安纳" }, { "city_1": "伊利诺伊", "city_2": "肯塔基" }, { "city_1": "印第安纳", "city_2": "俄亥俄" }, { "city_1": "印第安纳", "city_2": "肯塔基" }, { "city_1": "俄亥俄", "city_2": "宾夕法尼亚" }, { "city_1": "俄亥俄", "city_2": "西弗吉尼亚" }, { "city_1": "俄亥俄", "city_2": "肯塔基" }, { "city_1": "宾夕法尼亚", "city_2": "纽约" }, { "city_1": "宾夕法尼亚", "city_2": "西弗吉尼亚" }, { "city_1": "西弗吉尼亚", "city_2": "弗吉尼亚" }, { "city_1": "西弗吉尼亚", "city_2": "肯塔基" }, { "city_1": "弗吉尼亚", "city_2": "北卡罗来纳" }, { "city_1": "弗吉尼亚", "city_2": "田纳西" }, { "city_1": "弗吉尼亚", "city_2": "肯塔基" }, { "city_1": "北卡罗来纳", "city_2": "南卡罗来纳" }, { "city_1": "北卡罗来纳", "city_2": "田纳西" }, { "city_1": "北卡罗来纳", "city_2": "佐治亚" }, { "city_1": "南卡罗来纳", "city_2": "佐治亚" }, { "city_1": "佐治亚", "city_2": "阿拉巴马" }, { "city_1": "佐治亚", "city_2": "佛罗里达" }, { "city_1": "佐治亚", "city_2": "田纳西" }, { "city_1": "佛罗里达", "city_2": "阿拉巴马" }, { "city_1": "阿拉巴马", "city_2": "密西西比" }, { "city_1": "阿拉巴马", "city_2": "田纳西" }, { "city_1": "密西西比", "city_2": "路易斯安那" }, { "city_1": "密西西比", "city_2": "田纳西" }, { "city_1": "密西西比", "city_2": "阿肯色" }, { "city_1": "路易斯安那", "city_2": "阿肯色" }, { "city_1": "阿肯色", "city_2": "田纳西" }, { "city_1": "田纳西", "city_2": "肯塔基" }],
      // 存储从SVG提取的州信息
      stateInfo: [],
      stateMap: {},
      stateNameMap: {},
      players: [],
      playersMap:{},
      gameStarted: false,
      currentTurn: 0,
      global_lines: [],
      isPaused: false, // 添加暂停状态变量
      commentaryResult: '',
      armies: [],
      mapSize: { width: 1300, height: 900 },
      currentSvgDom: null,
      bufferSvgDom: null,
      baseSvgText: null,
      pathCenterCache:{},
      round:0,
      refreshInterval:1000,
      loading: true,
      armySvgDocument:null,
      command_history:[],
      game_events:[],
    }
  },
  watch: {

    // commentaryResult() {
    //   this.$nextTick(() => {
    //     this.scrollToBottom('commentary');
    //   });
    // },
    // game_events() {
    //   this.$nextTick(() => {
    //     this.scrollToBottom('gameEventsRef');
    //   });
    // },
    // global_lines() {
    //   this.$nextTick(() => {
    //     this.scrollToBottom('commentary');
    //   });
    // },
  },
  methods: {
    scrollToBottom(refName) {
      const element = this.$refs[refName];
      if (element) {
        element.scrollTop = element.scrollHeight;
      }
    },

    async startGame() {
      try {
        this.loading = false;
        await this.loadSvgMap();
        setTimeout(() => {
          fetch('/api/initialize_game_from_frontend', {
            'method': 'POST',
            'headers': {
              'Content-Type': 'application/json',
            },
            'body': JSON.stringify({
              'stateInfo': this.stateInfo,
              'roads': this.roads
            })
          });
          // 启动定时器刷新游戏状态
          this.timerId = setInterval(() => this.fetchGameState(), this.refreshInterval);
        }, 2000);
      } catch (err) {
        console.error('游戏初始化失败:', err);
      }
    },
    // 添加暂停游戏方法
    async pauseGame() {
      try {
        await fetch('/api/pause_game', { method: 'POST' });
        this.isPaused = true;
        // 暂停时清除定时器
        if (this.timerId) {
          clearInterval(this.timerId);
          this.timerId = null;
        }
      } catch (err) {
        console.error('暂停游戏失败:', err);
      }
    },
    async loadGame() {
      try {
        await this.loadSvgMap();
        this.gameStarted = true;
        const response = await fetch('/api/load_game', { method: 'POST' });
        const result = await response.json();
        if (result.status === 'success') {
          this.fetchGameState(); // 加载后刷新游戏状态
          alert('游戏已从存档加载');
        } else {
          alert('加载存档失败: ' + result.message);
        }
      } catch (err) {
        console.error('加载存档失败:', err);
        alert('加载存档时发生错误');
      }
    },
    async continueGame() {
      await this.loadSvgMap();
      this.gameStarted = true;
      if (this.isPaused) {
        // 如果游戏处于暂停状态，发送恢复请求
        fetch('/api/resume_game', { method: 'POST' })
          .catch(err => console.error('恢复游戏失败:', err));
      }
      this.fetchGameState();
      this.timerId = setInterval(() => this.fetchGameState(), this.refreshInterval);
    },
    formatTroops(army_troops) {
      // 增强健壮性，确保troops是有效数字
      if (army_troops == undefined || army_troops == null || typeof army_troops === 'undefined') {
        return '0';
      }
      const troops = Number(army_troops);
      // 单位转为万,保留一位小数
      if(troops > 10000){
        const troops_wan = troops/10000;
        return troops_wan.toFixed(1) + '万';
      } else {
        return troops;
      }
    },
    async fetchGameState() {
      try {
        const response = await fetch('/api/get_game_state');
        const gameState = await response.json();
        this.stateInfo = gameState.cities;
        this.stateInfo.forEach(state => {
          this.stateMap[state.id] = state;
          this.stateNameMap[state.nameZh] = state;
        });
        this.players = gameState.players;
        this.players.forEach(player => {
          this.playersMap[player.name] = player;
        });

        // this.roads = gameState.roads;
        this.armies = gameState.armies;
        this.currentTurn = gameState.current_turn;
        this.mapSize = gameState.mapSize;
        this.global_lines = gameState.global_lines;
        this.isPaused = gameState.is_paused;
        this.commentaryResult = gameState.commentary_result; // 添加解说结果
        this.command_history = gameState.command_history;
        this.game_events = gameState.game_events;
        // 创建缓冲区SVG并处理
        this.round = this.round +1;
        const mapContainer = document.getElementById("map-container");
        var parser = new DOMParser();
        // 地图区域的绝对定位
        var doc = parser.parseFromString(`<div id="mapSvg${this.round}" class="map-svg" style="position:absolute;top:0xp;left-380px;width:100%;height:100%;z-index:-1"></div>`, "text/html");
        var parsedElement = doc.body.firstChild;
        mapContainer.appendChild(parsedElement);
        
        this.bufferSvgDom = this.parseSvgText(this.baseSvgText);
        this.prepareSvgContainer(this.bufferSvgDom);
        this.setupSvgDimensions(this.bufferSvgDom);
        this.processSvgPaths(this.bufferSvgDom);
        this.showArmies(this.bufferSvgDom, this.armies);
        setTimeout(()=>{
          // 替换当前SVG
          this.getNextSvgContainer().style.zIndex = 1;
          if(this.round > 0){
            const oldRound = this.round-1;
            const oldDom = document.getElementById("mapSvg"+oldRound)
            setTimeout(()=>{
              if(oldDom != null && oldDom != undefined){
                oldDom.remove();
              }
            },50)
          }
          this.getNextSvgContainer().style.zIndex = 0;
          this.currentSvgDom = this.bufferSvgDom;
          this.bufferSvgDom = null;
        },100)
      } catch (err) {
        console.error('获取游戏状态失败:', err);
      }
    },
    getNextSvgContainer(){
      return document.getElementById("mapSvg"+this.round);
    },
    loadSvgMap() {
      console.log('Starting SVG map loading process');
      return this.fetchSvgText()
        .then(svgText => {
          this.baseSvgText = svgText;
          return this.parseSvgText(svgText);
        })
        .then(svgElement => {
          this.prepareSvgContainer(svgElement);
          this.setupSvgDimensions(svgElement);
          this.initializeSvgOnload(svgElement);
          this.startSvgReadinessCheck(svgElement);
          console.log(this.stateInfo);
          // 处理道路数据，添加city1_id和city2_id
          this.enrichRoadsData();
        })
        .catch(error => {
          this.handleError('svg_load_failed', 'SVG地图加载失败', error);
          throw error;
        });
    },
    enrichRoadsData() {
      if (this.stateInfo.length === 0) {
        // 如果stateInfo还未加载，延迟后重试
        setTimeout(this.enrichRoadsData, 1000);
        return;
      }
      this.stateInfo.forEach(state => {
          this.stateMap[state.id] = state;
          this.stateNameMap[state.nameZh] = state;
      });
      // 创建州名称到ID的映射，提高查找效率
      const stateNameToIdMap = new Map();
      this.stateInfo.forEach(state => {
        if (state.nameZh) {
          stateNameToIdMap.set(state.nameZh, state.id);
        }
      });

      // 丰富roads数据
      this.roads = this.roads.map(road => {
        const city1 = this.stateNameMap[road.city_1] || null;
        const city2 = this.stateNameMap[road.city_2] || null;
        // 记录未找到匹配ID的情况
        if (city1 === null) {
          console.warn(`未找到州 ${road.city_1} 的ID`);
        }
        if (city2 === null) {
          console.warn(`未找到州 ${road.city_2} 的ID`);
        }
        const city1Id = city1.id
        const city2Id = city2.id
        // 计算两个城市的距离 
        var distance = Math.sqrt(Math.pow(city1.x - city2.x, 2) + Math.pow(city1.y - city2.y, 2));
        road["length"] = distance;
        road["city1_id"] = city1Id;
        road["city2_id"] = city2Id;
        return road;
      })
      console.log(this.roads);
    },
    fetchSvgText() {
      return fetch(this.config.svgFilePath)
        .then(response => {
          if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
          return response.text();
        });
    },

    parseSvgText(svgText) {
      const parser = new DOMParser();
      const svgDoc = parser.parseFromString(svgText, 'image/svg+xml');
      if (svgDoc.documentElement.tagName === 'parsererror') {
        console.error('SVG parsing error:', svgDoc.documentElement.textContent);
        this.handleError('svg_parse_error', 'SVG文件解析失败');
        throw new Error('SVG parsing failed');
      }
      return svgDoc.documentElement;
    },

    setupSvgDimensions(svgElement) {
      const container = this.getNextSvgContainer();
      if (!container) return;

      const rect = container.getBoundingClientRect();
      if (rect.width > 0 && rect.height > 0) {
        if (!svgElement.hasAttribute('width')) {
          svgElement.setAttribute('width', '100%');
        }
        if (!svgElement.hasAttribute('height')) {
          svgElement.setAttribute('height', '100%');
        }
        svgElement.style.width = '100%';
        svgElement.style.height = '100%';
        svgElement.style.display = 'block';
      }
    },

    initializeSvgOnload(svgElement) {
      svgElement.onload = () => {
        if (!svgElement.hasAttribute('viewBox')) {
          const bbox = svgElement.getBBox();
          if (bbox.width > 0 && bbox.height > 0) {
            svgElement.setAttribute('viewBox', `${bbox.x} ${bbox.y} ${bbox.width} ${bbox.height}`);
          } else {
            svgElement.setAttribute('viewBox', '0 0 1000 600');
          }
        }

        if (!svgElement.hasAttribute('preserveAspectRatio')) {
          svgElement.setAttribute('preserveAspectRatio', 'xMidYMid meet');
        }
        this.processSvgPaths(svgElement);
      };
    },
    startSvgReadinessCheck(svgElement) {
      const checkSvgReady = (attempt = 0) => {
        console.log(`Checking SVG readiness - Attempt ${attempt + 1}`);
        const maxAttempts = 30;
        const delayMs = 150;
        const container = this.getNextSvgContainer();
        const svgRect = svgElement.getBoundingClientRect();
        const containerReady = container && container.offsetWidth > 0 && container.offsetHeight > 0;
        const svgReady = svgRect.width > 0 && svgRect.height > 0;

        if ((containerReady && svgReady) || attempt >= maxAttempts) {
          console.log(`SVG readiness check complete - Attempt ${attempt + 1}, Container ready: ${containerReady}, SVG ready: ${svgReady}`);
          if (containerReady && svgReady) {
            console.log('Initiating SVG path processing');
            svgElement.onload();
          } else {
            const errorMsg = !containerReady ? '容器尺寸未就绪' : 'SVG加载未完成';
            this.handleError('svg_load_timeout', `SVG加载超时(${errorMsg})，已尝试${maxAttempts}次`);
          }
          return;
        }

        // setTimeout(() => checkSvgReady(attempt + 1), delayMs);
      };

      checkSvgReady();
    },

    processSvgPaths(svgElement) {
      // 使用重试机制确保路径元素已加载
      const maxRetries = 10; // 增加重试次数
      const retryDelayMs = 200; // 延长重试延迟

      const findAndProcessPaths = (attempt = 0) => {
        // console.log(`Processing SVG paths - Retry count: ${attempt}`);
        const paths = Array.from(svgElement.getElementsByTagNameNS(this.config.SVG_NAMESPACE, 'path'));
        // console.log(`Found ${paths.length} path elements`);

        if (paths.length > 0) {
          paths.forEach((path, index) => {
            this.processSinglePath(svgElement, path, index);
          });
        } else if (attempt < maxRetries) {
          console.warn(`No path elements found, retry count: ${attempt}`);
          // setTimeout(() => findAndProcessPaths(attempt + 1), retryDelayMs);
        } else {
          this.handleError('no_paths_found', `未找到任何SVG路径元素，已尝试${maxRetries}次`);
        }
      };

      findAndProcessPaths();
    },
    /**
       * 统一错误处理方法
       * @param {string} errorCode - 错误代码
       * @param {string} message - 错误消息
       * @param {Error} [error] - 错误对象（可选）
       */
    handleError(errorCode, message, error = null) {
      const errorDetails = error ? `: ${error.message}` : '';
      console.error(`[${errorCode}] ${message}${errorDetails}`);
      // 可在此处添加统一的错误上报或用户提示逻辑
    },
    // 实现显示军队
    showArmies(bufferSvgDom, armies){
      armies.forEach(army => {
        var player_name = army.player_name;
        var player = this.playersMap[player_name];
        
        // 创建军队组元素
        const armyGroup = bufferSvgDom.ownerDocument.createElementNS(this.config.SVG_NAMESPACE, 'g');
        armyGroup.setAttribute('class', 'army-group');
        armyGroup.setAttribute('transform', `translate(${army.current_x}, ${army.current_y})`);

        // 根据 this.armySvgDocument 添加军队svg图标
        const svgElement = bufferSvgDom.ownerDocument.importNode(this.armySvgDocument['svgElement'], true);
        // 设置SVG属性
        svgElement.setAttribute('width', '38');
        svgElement.setAttribute('height', '38');
        svgElement.setAttribute('x', '-10');
        svgElement.setAttribute('y', '-10');

        // 设置SVG颜色
        const paths = svgElement.querySelectorAll('path, circle, rect, polygon, line');
        paths.forEach(path => {
          path.setAttribute('fill', player['color']);
          path.setAttribute('stroke', player['color']);
        });
        armyGroup.appendChild(svgElement);

        // 添加军队信息文本
        const textGroup = bufferSvgDom.ownerDocument.createElementNS(this.config.SVG_NAMESPACE, 'text');
        textGroup.setAttribute('x', '20');
        textGroup.setAttribute('y', '0');
        textGroup.setAttribute('text-anchor', 'start');
        textGroup.setAttribute('dominant-baseline', 'middle');
        textGroup.style.fontSize = this.config.textStyle.fontSize;
        textGroup.style.fill = this.config.textStyle.color;
        textGroup.style.stroke = this.config.textStyle.color;

        // 创建玩家名称文本
        // const nameTspan = bufferSvgDom.ownerDocument.createElementNS(this.config.SVG_NAMESPACE, 'tspan');
        // nameTspan.setAttribute('x', '20');
        // nameTspan.setAttribute('dy', '0em');
        // nameTspan.textContent = army.player_name;
        // textGroup.appendChild(nameTspan);

        // 创建兵力文本
        const troopsTspan = bufferSvgDom.ownerDocument.createElementNS(this.config.SVG_NAMESPACE, 'tspan');
        troopsTspan.setAttribute('x', '20');
        troopsTspan.setAttribute('dy', '1.2em');
        const troops = this.formatTroops(army.troops);
        troopsTspan.textContent = `${troops.toLocaleString()}`;

        textGroup.appendChild(troopsTspan);
        armyGroup.appendChild(textGroup);
        armyGroup.style.zIndex = 20;
        bufferSvgDom.appendChild(armyGroup);
      });
    },
    /**
     * 准备SVG容器并添加SVG元素
     * @param {SVGElement} svgElement - SVG根元素
     */
    prepareSvgContainer(svgElement) {
      const container = this.getNextSvgContainer();
      if (!container) {
        this.handleError('container_not_found', 'SVG容器未找到（ref不存在）');
        return;
      }
      container.innerHTML = '';
      container.appendChild(svgElement);

      // 触发重排以确保尺寸计算准确
      container.offsetHeight; // 强制浏览器重排

      // 检查容器尺寸是否有效
      const rect = container.getBoundingClientRect();
      if (rect.width === 0 || rect.height === 0) {
        this.handleError('container_size_zero', 'SVG容器尺寸为零，无法正确渲染');
      }
    },

    /**
     * 设置路径元素的填充颜色样式
     * @param {SVGElement} path - 路径元素
     * @param {string} color - 填充颜色
     */
    setPathStyle(path, color) {
      // 移除可能存在的fill属性，确保样式优先
      path.removeAttribute('fill');

      let currentStyle = path.getAttribute('style') || '';
      currentStyle = currentStyle.replace(/fill\s*:\s*[^;]+;/gi, '').trim();
      const newStyle = currentStyle ? `${currentStyle}; fill: ${color}; stroke: #b3fff5; stroke-width: 1;` : `fill: ${color}; stroke: #b3fff5; stroke-width: 1;`;
      path.setAttribute('style', newStyle);
    },

    /**
     * 提取州信息并返回格式化对象
     * @param {SVGElement} path - 州路径元素
     * @param {string} color - 州颜色
     * @returns {Object|null} 州信息对象或null
     */
    extractStateInfo(path, color, x, y, index) {
      const stateId = path.id || path.getAttribute('data-id');
      const stateName = path.getAttribute('data-name');
      if (!stateId) {
        console.error('Path missing ID attribute', path);
      }
      if (!stateName) {
        console.error('Path missing data-name attribute', path);
      }
      if (!stateId || !stateName) return null;
      var name = path.getAttribute('data-name-zh') || ''
      return {
        id: index + 1,
        name: name,
        nameEn: stateName,
        nameZh: name,
        garrisons: {},
        growth_rate: 1000,
        x: x,
        y: y
      };
    },

    /**
     * 处理单个路径元素的完整逻辑
     * @param {SVGElement} svgElement - SVG根元素
     * @param {SVGElement} path - 单个路径元素
     * @param {number} index - 路径索引
     */
    processSinglePath(svgElement, path, index) {
      // 检查路径是否有必要的属性，添加重试机制
      const maxRetries = 3;
      const retryDelayMs = 100;

      const processWithRetry = async (attempt = 0) => {
        const pathId = path.getAttribute('id') || path.getAttribute('data-id') || index.toString();
        // console.log(`Processing path - ID: ${pathId}, Retry: ${attempt}`);
        // 使用路径唯一ID生成种子，确保每个州颜色不同
        const stateName = path.getAttribute('data-name');

        // 检查必要属性是否存在
        if (!pathId || !stateName) {
          if (attempt < maxRetries) {
            // setTimeout(() => processWithRetry(attempt + 1), retryDelayMs);
            return;
          } else {
            this.handleError('missing_path_attributes', `路径${index}缺少必要属性(id/data-id或data-name)，已尝试${maxRetries}次`);
            return;
          }
        }

        // 获取州信息以确定拥有者颜色 
        const state = this.stateInfo.find(s => s.id === index + 1);
        const color = state ? this.getOwnerColor(state) : this.config.no_owner_color;
        
        // 设置路径样式
        this.setPathStyle(path, color);

        // 获取坐标
        const { centerX, centerY } = await this.calculatePathCenter(path);

        // 提取并存储州信息
        const stateInfoFromSVG = this.extractStateInfo(path, color, centerX, centerY, index);
        var stateInfo = stateInfoFromSVG;

        if(this.stateMap[stateInfoFromSVG.id] != undefined ){
          stateInfo = this.stateMap[stateInfoFromSVG.id];
        }
        if (stateInfo) {
          this.stateInfo.push(stateInfo);
        }

        // 创建州名称文本元素
        try {
            this.createStateTextElement(svgElement, path, stateInfo);
        } catch (error) {
            console.error('创建州名称文本元素失败:', error);
            // 可以选择记录错误日志或进行其他错误处理
        }
        
        // 检查是否有多个玩家军队，显示战斗图标
        if (stateInfo && stateInfo.garrisons && Object.keys(stateInfo.garrisons).length > 1) {
          const center = { x: centerX, y: centerY };
          if (center) {
            const battleIcon = document.createElementNS(this.config.SVG_NAMESPACE, 'image');
            battleIcon.setAttributeNS('http://www.w3.org/1999/xlink', 'href', require('@/assets/images/boom.svg'));
            battleIcon.setAttribute('x', (center.x - 20).toString());
            battleIcon.setAttribute('y', (center.y - 38).toString());
            battleIcon.setAttribute('width', '30');
            battleIcon.setAttribute('height', '30');
            svgElement.appendChild(battleIcon);
          }
        }

        // 记录州处理日志
        this.logStateProcessing(stateInfo, color);
      };

      processWithRetry().catch(error => {
        this.handleError('path_processing_failed', '路径处理失败', error);
      });
    },

    /**
     * 创建并配置文本元素
     * @param {SVGElement} svgElement - SVG根元素
     * @param {SVGElement} path - 路径元素
     * @param {string} textContent - 文本内容
     * @returns {SVGElement} 配置好的文本元素
     */
    async createTextElement(svgElement, path, textContent) {
      // 创建文本元素
      const text = svgElement.ownerDocument.createElementNS(this.config.SVG_NAMESPACE, 'text');

      // 计算路径中心位置（带重试机制）
      const { centerX, centerY } = await this.calculatePathCenter(path);

      // 设置文本属性
      text.setAttribute('x', centerX.toString());
      text.setAttribute('y', centerY.toString());
      text.setAttribute('text-anchor', 'middle');
      text.setAttribute('dominant-baseline', 'middle');
      text.setAttribute('text-rendering', 'crispEdges');
      // 减小字体粗细
      text.setAttribute('font-weight', '100');
      // 设置文本内容，支持换行
      text.textContent = '';
      const lines = textContent.split('\n');
      
      lines.forEach((line, index) => {
        const tspan = svgElement.ownerDocument.createElementNS(this.config.SVG_NAMESPACE, 'tspan');
        tspan.setAttribute('x', centerX.toString());
        tspan.setAttribute('dy', index === 0 ? '0em' : '1.2em');
        tspan.textContent = line;
        if(index>0){
          tspan.style.fontFamily = this.config.textStyle.fontFamily;
          tspan.style.fontWeight = this.config.textStyle.fontWeight;
          tspan.style.fontSize = this.config.textStyle.fontSize;
          tspan.style.stroke = this.config.textStyle.color;
        }
        text.appendChild(tspan);
      });

      text.style.fontFamily = this.config.textStyle.fontFamily;
      text.style.fontWeight = this.config.textStyle.fontWeight;
      text.style.fontSize = this.config.textStyle.fontSize;
      text.style.color = this.config.textStyle.color;
      text.style.stroke = this.config.textStyle.color;

      return text;
    },

    /**
     * 计算路径元素的中心位置
     * @param {SVGElement} path - 路径元素
     * @returns {{centerX: number, centerY: number}} 中心坐标
     */
    calculatePathCenter(path) {
      const maxRetries = 5; // 增加到5次重试
      const retryDelayMs = 50; // 增加延迟到100ms
      const pathName = path.getAttribute('data-name');
      if(pathName == undefined){
        debugger
      }
      // if (this.pathCenterCache[pathName]) {
      //   return this.pathCenterCache[pathName];
      // }

      const calculateWithRetry = (attempt) => {
        try {
          const bbox = path.getBBox();

          // 验证边界框有效性
          if (bbox.width === 0 || bbox.height === 0) {
            if (attempt < maxRetries) {
              // 问题点
              console.log(`${attempt}-${maxRetries}`)
              return new Promise(resolve => {
                setTimeout(() => {
                  resolve(calculateWithRetry(attempt + 1));
                }, retryDelayMs);
              });
            } else {
              this.handleError('invalid_path_bbox', `路径${path.id || '未知'}边界框尺寸为零，已尝试${maxRetries}次`);
              return { centerX: 0, centerY: 0 };
            }
          }
          this.pathCenterCache[pathName] = { centerX: bbox.x + bbox.width / 2, centerY: bbox.y + bbox.height / 2 };
          return { centerX: bbox.x + bbox.width / 2, centerY: bbox.y + bbox.height / 2 };
        } catch (e) {
          if (attempt < maxRetries) {
            return new Promise(resolve => {
              setTimeout(() => {
                resolve(calculateWithRetry(attempt + 1));
              }, retryDelayMs);
            });
          } else {
            this.handleError('bbox_calculation_failed', `路径边界框计算失败，已尝试${maxRetries}次`, e);
            return { centerX: 0, centerY: 0 };
          }
        }
      };

      return calculateWithRetry(0);
    },

    /**
     * 记录州处理日志信息
     * @param {Object|null} stateInfo - 州信息对象
     * @param {string} color - 州颜色
     */
    logStateProcessing(stateInfo, color) {
      if (!stateInfo) return;
      // console.log(`设置州 ${stateInfo.name} ${stateInfo.nameZh} (${stateInfo.id}) 颜色: ${color}`);
    },

    /**
       * 生成初始随机数种子
       * @param {number} hash - 路径ID哈希值
       * @param {number} index - 路径索引
       * @returns {number} 初始种子值
       */
    generateInitialSeed(hash, index) {
      return hash + index + Math.random();
    },

    /**
     * 根据路径ID生成哈希值
     * @param {string} pathId - 路径元素ID
     * @returns {number} 32位整数哈希值
     */
    generateHashFromId(pathId) {
      let hash = 0;
      for (let i = 0; i < pathId.length; i++) {
        const char = pathId.charCodeAt(i);
        hash = ((hash << 5) - hash) + char;
        hash = hash & hash; // 转换为32位整数
      }
      return hash;
    },

    /**
     * 使用线性同余生成器(LCG)生成随机数
     * @param {number} seed - 随机数种子
     * @returns {Object} 包含随机数和新种子的对象
     */
    getRandomNumber(seed) {
      const a = 1664525;
      const c = 1013904223;
      const m = Math.pow(2, 32);
      const newSeed = (a * seed + c) % m;
      return { random: newSeed / m, newSeed };
    },

    /**
     * 生成州路径的随机颜色
     * @param {string} pathId - 路径元素ID
     * @param {number} index - 路径索引
     * @returns {string} HSL颜色字符串
     */
    generateStateColor(pathId, index) {
      // 使用路径唯一ID生成种子，确保每个州颜色不同
      let hash = 0;
      for (let i = 0; i < pathId.length; i++) {
        const char = pathId.charCodeAt(i);
        hash = ((hash << 5) - hash) + char;
        hash = hash & hash; // 转换为32位整数
      }
      const seed = this.generateInitialSeed(hash, index);

      // 生成鲜明且避免接近白色的颜色
      let { random: hueRandom, newSeed } = this.getRandomNumber(seed);
      const hue = Math.floor(hueRandom * 360);

      let saturationRandom;
      ({ random: saturationRandom, newSeed } = this.getRandomNumber(newSeed));
      const saturation = this.config.colorConfig.saturationRange[0] + Math.floor(saturationRandom * (this.config.colorConfig.saturationRange[1] - this.config.colorConfig.saturationRange[0]));

      let lightnessRandom;
      ({ random: lightnessRandom, newSeed } = this.getRandomNumber(newSeed));
      const lightness = this.config.colorConfig.lightnessRange[0] + Math.floor(lightnessRandom * (this.config.colorConfig.lightnessRange[1] - this.config.colorConfig.lightnessRange[0]));;
      return `hsl(${hue}, ${saturation}%, ${lightness}%)`;
    },

    /**
     * 创建州名称文本元素并添加到SVG中
     * @param {SVGElement} svgElement - SVG根元素
     * @param {SVGElement} path - 州路径元素
     * @param {string} stateName - 州英文名
     * @param {string} nameZh - 州中文名
     */
    createStateTextElement(svgElement, path, stateInfo) {
      // 使用双重requestAnimationFrame确保SVG路径完全渲染
      requestAnimationFrame(async () => {
        try {
          // 验证文本内容
          if (!stateInfo['nameZh'] && !stateInfo['stateName']) {
            this.handleError('missing_text_content', `路径${path.id || '未知'}缺少文本内容`);
            return;
          }

          // 验证父节点是否在DOM中
          if (!document.contains(path.parentNode)) {
            this.handleError('parent_node_not_in_dom', `路径${path.id || '未知'}的父节点不在DOM中`);
            return;
          }
          // 州兵力显示
          var stateName = stateInfo['nameZh'];
          var content = `${stateName} \n`;
          if(stateInfo['garrisons'] != undefined){
            const garrisons = stateInfo['garrisons'];
            for(let key in garrisons){
              const troops = this.formatTroops(garrisons[key])
              content += key + ":" + troops + "\n";
            }

          }
          // 创建并配置文本元素
          const text = await this.createTextElement(svgElement, path, content);
          // 添加到路径的父节点以继承坐标变换
          path.parentNode.appendChild(text);
        } catch (e) {
          this.handleError('text_creation_failed', '处理州名称文本失败', e);
        }
      });
    },
    /**
     * 根据军队数量确定州的拥有者并返回对应颜色
     */
    getOwnerColor(state) {
      const garrisons = state.garrisons || {};
      let maxTroops = 0;
      let ownerName = null;

      // 找出拥有最多军队的玩家名称
      for (const [player, troops] of Object.entries(garrisons)) {
        if (troops > maxTroops) {
          maxTroops = troops;
          ownerName = player;
        }
      }

      // 如果没有拥有者，返回默认颜色
      if (!ownerName) {
        return this.config.no_owner_color; // 默认灰色
      }

      // 在玩家列表中查找对应的玩家颜色
      const owner = this.players.find(p => p.name === ownerName);
      if(owner != undefined && ('background_color' in owner)){
        return owner['background_color'];
      }
      return owner ? owner.color : this.config.no_owner_color; // 找不到玩家时使用默认颜色
    },
    // 加载 SVG 文件
    async loadSVG(svgUrl) {
        try {
            const response = await fetch(svgUrl)
            const svgText = await response.text();
            return svgText;
        } catch (error) {
            console.error('加载 SVG 文件失败:', error);
            return null;
        }
    },
    // 解析 SVG 文件
    parseSVG(svgText) {
        const parser = new DOMParser();
        const svgDoc = parser.parseFromString(svgText, "image/svg+xml");
        const svgElement = svgDoc.documentElement;

        // 提取 SVG 中的所有路径
        const paths = svgElement.querySelectorAll('path');
        return { svgElement, paths };
    },
  },
  mounted() {
    Promise.all([
      this.loadSVG(require('@/assets/images/solider.svg'))
    ]).then(([armySvgText]) => {
      if (armySvgText) {
        this.armySvgDocument = this.parseSVG(armySvgText);
      }
    });

  },
  beforeUnmount() {
    if (this.timerId) {
      clearInterval(this.timerId);
    }
  },
  computed: {
    gameDate() {
      return `${this.currentTurn}回合`;
    },
    // 按乓兵总数降序排序玩家
    sortedPlayers() {
      // 创建副本避免修改原数组
      return [...this.players].sort((a, b) => {
        const troopsA = a.total_troops || 0;
        const troopsB = b.total_troops || 0;
        return troopsB - troopsA; // 降序排列
      });
    }
  }
}


</script>

<style scoped>
@font-face {
  font-family: 'YuFanXiLiu';
  src: url('@/assets/font/YuFanXiLiu.otf') format('opentype');
  font-weight: normal;
  font-style: normal;
}
@font-face {
  font-family: 'AlibabaPuHuiTi-3-35-Thin';
  src: url('@/assets/font/AlibabaPuHuiTi-3-35-Thin.woff2');
  font-weight: normal;
  font-style: normal;
}

.american-civil-war-map {
  width: 100%;
  height: 100vh;
  padding: 0px;
}

#map-container {
  position: relative;
  top: -90px;
  left:-320px;
  width: 1800px;
  height: 1000px;
  margin: 0px;
  overflow: hidden;
}
.map-svg{
  position: relative;
  top: 0px;
  left:-380px;
  width: 100%;
  height: 100%;
}

.game-info-panel {
  display: flex;
  flex-direction:column;
  padding: 0px;
}

.game-container {
  width: 100%;
  height: 600px;
}
.commentary-factions-total{
  display: flex;
  flex-direction:row;
  width:100%; 
}
.game-command-history {
  flex:6;
  height: 350px;
  overflow-y: auto;
  padding: 0px;
  margin: 0px;
  padding:5px;
  z-index: -1 ;
}
.player-factions {
  flex:5;
  display: flex;
  flex-direction:column;
  width:300px;
  margin: 0px;
  padding: 0px;
}

.faction-item {
  width:100%;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  color:  #000 !important;
  padding: 0px;
}
.player-info-basic{
  width:100%;
  display:flex;
}
.player-lines {
  margin-top: 8px;
  font-size: 12px;
  width: 100%;
  height:300px;
  overflow: auto;
}
.latest-line {
  font-weight: bold;
  font-size: 18px;
  margin-top: 4px;
}

.defeated-row {
  background-color: #e0e0e0;
}

.start-game-btn {
  background-color: #4CAF50;
  color: white;
  border: none;
  padding: 5px;
  margin: 5px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  margin-top: 10px;
}
.start-game-btn:hover {
  background-color: #45a049;
}

.color-indicator {
  width: 100%;
  height: 15px;
  margin-right: 5px;
}

.game-progress {
  margin-top: 20px;
  padding-top: 10px;
}
.debug-info{
  display: block;
}
.debug-info>p{
  margin:1px;
  padding:0px;
}
.game-title{
  background-image: url('../assets/images/game-title.png');
  background-size: 36% 100%;
  background-position: 50%;
  height: 70px;
  z-index: 10;
}
</style>