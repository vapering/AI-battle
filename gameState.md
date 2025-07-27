下面是接口 /api/get_game_state 的返回报文样例：
{
  "armies": [
    {
      "current_x": 555.8509824643527, 
      "current_y": 204.550338752599, 
      "dest_city_id": 8, 
      "direction_x": -0.9801851112533467, 
      "direction_y": 0.19808368856941327, 
      "distance_remaining": 345.1747585386936, 
      "id": 0, 
      "player_name": "里帕布自由军", 
      "required_turns": 39, 
      "speed": 9, 
      "start_city_id": 38, 
      "troops": 20000
    }, 
    {
      "current_x": 234.37500857467086, 
      "current_y": 281.90872326171007, 
      "dest_city_id": 8, 
      "direction_x": -0.8824978787481215, 
      "direction_y": -0.47031637650103764, 
      "distance_remaining": 19.10393850955103, 
      "id": 1, 
      "player_name": "Grok新世界", 
      "required_turns": 3, 
      "speed": 9, 
      "start_city_id": 23, 
      "troops": 15000
    }
  ], 
  "cities": [
    {
      "garrisons": {
        "民兵": 50000
      }, 
      "growth_rate": 1000, 
      "id": 1, 
      "name": "马萨诸塞州", 
      "nameEn": "Massachusetts", 
      "nameZh": "马萨诸塞州", 
      "x": 938.6463928222656, 
      "y": 137.32663345336914
    }, 
    {
      "garrisons": {
        "民兵": 50000
      }, 
      "growth_rate": 1000, 
      "id": 2, 
      "name": "明尼苏达州", 
      "nameEn": "Minnesota", 
      "nameZh": "明尼苏达州", 
      "x": 610.572998046875, 
      "y": 124.90254974365234
    }, 
    {
      "garrisons": {
        "民兵": 50000
      }, 
      "growth_rate": 1000, 
      "id": 3, 
      "name": "蒙大拿州", 
      "nameEn": "Montana", 
      "nameZh": "蒙大拿州", 
      "x": 386.2602233886719, 
      "y": 103.88835906982422
    }
  ], 
  "command_history": [
    {
      "command": "派遣20000兵力从加利福尼亚州前往内华达州", 
      "player_name": "得莫克阵线", 
      "result": "success", 
      "turn": 55
    }, 
    {
      "command": "派遣4000兵力从加利福尼亚州前往得克萨斯州", 
      "player_name": "得莫克阵线", 
      "result": "success", 
      "turn": 55
    }
  ], 
  "commentary_result": "", 
  "current_turn": 57, 
  "global_lines": [
    "[2025-07-08 21:47:23] 里帕布自由军: 里帕布勇士听令！从纽约州起兵直捣加利福尼亚，叫那得莫克阵线尝尝厉害！", 
    "[2025-07-08 21:47:24] Grok新世界: 得州蛮夷，敢据沃土！今我师出 texas，兵锋直指加州，尔等鼠辈何不束手就擒？", 
    "[2025-07-08 21:47:33] 里帕布自由军: 里帕布勇士听令！两万雄师直扑加州，叫那得莫克见识我等锋芒！", 
    "[2025-07-08 21:47:34] 得莫克阵线: 得莫克的铁骑踏破西部荒野！Grok那群硅谷书呆子也配占得克萨斯？老子今天就用加州红杉木造棺材送你们上路！", 
    "[2025-07-08 21:47:39] Grok新世界: 兵发加州，势如破竹！我Groks大军所向披靡，尔等草寇岂能挡我锋芒？", 
    "[2025-07-08 21:47:45] 里帕布自由军: 里帕布勇士再出征，两万雄师砸向加州，得莫克别想逃！", 
    "[2025-07-08 21:47:55] Grok新世界: 再调三路大军，兵临加州城下！Grok铁骑誓破顽敌，得州雄师威震西疆！", 
    "[2025-07-08 21:47:58] 里帕布自由军: 里帕布勇士再度出击，两万雄师直捣加州，得莫克且看我等锐不可当！", 
    "[2025-07-08 21:47:58] 得莫克阵线: 得莫克铁骑听令！Grok那群硅谷书呆子也敢犯我加州？今日就用你们的血染红内华达沙漠！里帕布的自由军？哼，不过是群纽约的软脚虾！"
  ], 
  "is_paused": false, 
  "mapSize": {
    "height": 800, 
    "width": 1200
  }, 
  "players": [
    {
      "city_count": 1, 
      "color": "#7B68EE", 
      "leader": "里帕布", 
      "model": "doubao-seed-1-6-flash-250615", 
      "name": "里帕布自由军", 
      "slogan": "当有人拆掉十字架，而Grok妄想当上帝——记住！没有人比我更懂自由，我们需要世界上最锋利的矛！", 
      "start_city": "纽约州", 
      "total_troops": 6000, 
      "voice_id": "cosyvoice-v2-prefix-5ca2bc9e87c0436a85ae8dafe6cbad00"
    }, 
    {
      "city_count": 1, 
      "color": "#FF6347", 
      "leader": "拜登", 
      "model": "deepseek-chat", 
      "name": "得莫克阵线", 
      "slogan": "他们砸碎国会玻璃，他们妄想统治火星——而你的誓言是守护最后的共和之光！", 
      "start_city": "加利福尼亚州", 
      "total_troops": 17000, 
      "voice_id": "cosyvoice-v2-prefix-0b29c2570b86446c8c5abba6d05e939e"
    }, 
    {
      "city_count": 1, 
      "color": "#00CED1", 
      "leader": "马斯克", 
      "model": "qwen-plus-latest", 
      "name": "Grok新世界", 
      "slogan": "议会议员都在腐烂！臣服于数字世界的精准高效吧，Grok将统治一切！", 
      "start_city": "得克萨斯州", 
      "total_troops": 23000, 
      "voice_id": "cosyvoice-v2-prefix-6fefd4b472ce4b2da7448f2df134a494"
    }
  ], 
  "roads": [], 
  "turn_report": "第 57 回合简报：\n\n=== 基本信息 ===\n当前回合：57\n活跃玩家数：\n"
}