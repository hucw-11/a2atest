# 用 SVG 和原生 JavaScript 实现一只骑自行车的鹈鹕：从静态插画到 2D 动画

> 一只白色鹈鹕，骑着青绿色自行车，慢悠悠地经过海边。本文把这幅场景做成可以直接打开的 HTML：车轮旋转、双腿蹬踏、身体轻轻起伏，云朵与地面向后移动，还可以暂停、调整速度和回到起点。

**建议标签：** SVG、HTML、JavaScript、前端、2D 动画、创意编程

## 1. 先确定画面和交互

这次使用内联 SVG 绘制画面，用 CSS 完成页面布局，再用原生 JavaScript 驱动动画。不引入第三方库，不加载外部图片、字体或脚本。把文末代码保存成 `pelican-bicycle.html`，即可在浏览器中打开。

画面沿用一套柔和的海岸配色：米白色羽毛、橙黄色长嘴、青绿色车架、浅蓝绿色海面和暖沙色小路。鹈鹕的辨识点放在长嘴、下垂的喉囊、弯曲的脖子和宽大的身体上。

交互包含三个部分：

- **播放与暂停**：同时控制车轮、蹬踏、眨眼和背景移动。
- **骑行速度**：支持 0.5～2 倍速度，改变速度时保留当前动作进度。
- **回到起点**：重置距离和动画时间，保留当前速度与播放状态。

页面也读取系统的“减少动态效果”偏好：如果开启，初始显示静态画面，用户仍然可以手动播放。

## 2. 用 SVG 分层组织场景

SVG 使用 `viewBox="0 0 1000 800"`。绘制时以这个逻辑坐标系为基准，页面通过 CSS 调整显示尺寸。

这幅画从后往前依次绘制：天空、太阳与云朵，海面，沙地与滚动装饰，自行车车轮，远侧曲柄与腿，车架，鹈鹕身体和头部，近侧曲柄与腿，最后是握住车把的翅膀。

SVG 元素的书写顺序决定遮挡关系。把远侧腿放在车架后面、近侧腿放在车架前面，双腿就能呈现出前后关系。

车轮用 `<defs>` 定义，再通过 `<use>` 复用。每个车轮外面有两层分组：外层负责定位，内层负责旋转。

```html
<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#f5f3eb">
  <title>海岸漫游 · 鹈鹕骑自行车</title>
  <style>
    :root { color-scheme: light; --ink: #294c4d; --muted: #6a827b; --accent: #2b8278; }
    * { box-sizing: border-box; }
    body { margin: 0; background: #f5f3eb; color: var(--ink); font-family: "Segoe UI", "Microsoft YaHei", sans-serif; }
    main { max-width: 1060px; margin: auto; padding: 42px 28px 24px; }
    header { display: flex; align-items: end; justify-content: space-between; gap: 24px; margin-bottom: 24px; }
    .eyebrow { margin: 0 0 10px; color: var(--accent); font-size: 11px; font-weight: 700; letter-spacing: .23em; }
    h1 { margin: 0; font-size: clamp(26px, 4vw, 40px); font-weight: 600; letter-spacing: .03em; }
    .intro { margin: 0 0 3px; color: var(--muted); line-height: 1.8; font-size: 14px; }
    .scene { overflow: hidden; border: 1px solid #dce4d7; border-radius: 28px; background: #edf7f4; box-shadow: 0 18px 55px #294c4d0c; }
    .scene svg { display: block; width: 100%; height: auto; max-height: 68vh; min-height: 280px; }
    .controls { display: flex; align-items: center; flex-wrap: wrap; gap: 14px 20px; padding: 18px 24px; background: #fffdf5; border-top: 1px solid #e0e8da; }
    button { cursor: pointer; font: inherit; border: 0; border-radius: 24px; padding: 11px 20px; font-size: 14px; }
    #toggle { min-width: 108px; color: #fffdf5; background: var(--accent); }
    #reset { color: var(--ink); background: #eaf0e5; }
    button:hover { filter: brightness(.95); }
    button:focus-visible, input:focus-visible { outline: 3px solid #d5903e; outline-offset: 4px; }
    .speed { display: flex; align-items: center; gap: 12px; margin-left: auto; font-size: 13px; }
    input[type="range"] { width: clamp(95px, 15vw, 170px); accent-color: var(--accent); cursor: pointer; }
    output { width: 3.5em; font-variant-numeric: tabular-nums; }
    footer { display: flex; justify-content: space-between; flex-wrap: wrap; gap: 8px; padding: 18px 3px 0; font-size: 12px; color: var(--muted); }
    #status { margin: 0; }
    noscript p { padding: 0 24px 16px; color: var(--muted); }
    @media (max-width: 640px) {
      main { padding: 24px 14px; }
      header { display: block; }
      .intro { margin-top: 12px; }
      .scene { border-radius: 20px; }
      .controls { padding: 16px; gap: 12px; }
      .speed { margin-left: 0; width: 100%; }
      input[type="range"] { flex: 1; }
    }
  </style>
</head>
<body>
  <main>
    <header>
      <div><p class="eyebrow">PELICAN RIDING CLUB / 01</p><h1>海风正好，骑慢一点。</h1></div>
      <p class="intro">跟着鹈鹕，沿海岸兜个风。<br>今天的目的地，是好心情。</p>
    </header>
    <section class="scene" aria-label="鹈鹕的海边骑行">
<svg id="coastal-scene" xmlns="http://www.w3.org/2000/svg" width="1000" height="800" viewBox="0 0 1000 800" role="img" aria-labelledby="title description">
  <title id="title">鹈鹕骑自行车</title>
  <desc id="description">一只长着橙色大嘴的白色鹈鹕，骑着青绿色自行车，双腿交替蹬踏，车轮转动，云朵与海边小路向后移动。</desc>
  <defs>
    <linearGradient id="sky" x2="0" y2="1">
      <stop stop-color="#edf7f4"/>
      <stop offset="1" stop-color="#fff8e9"/>
    </linearGradient>
    <linearGradient id="feathers" x1="0" y1="0" x2=".8" y2="1">
      <stop stop-color="#fffef8"/>
      <stop offset="1" stop-color="#e0e9e2"/>
    </linearGradient>
    <linearGradient id="bill" x2="0" y2="1">
      <stop stop-color="#ffc65e"/>
      <stop offset="1" stop-color="#f49a42"/>
    </linearGradient>
    <linearGradient id="pouch" x2="0" y2="1">
      <stop stop-color="#f7b17a"/>
      <stop offset="1" stop-color="#e98a69"/>
    </linearGradient>
    <g id="wheel">
      <circle r="126" fill="#fffaf0" stroke="#304e51" stroke-width="15"/>
      <circle r="113" fill="none" stroke="#c4d3c9" stroke-width="3"/>
      <g stroke="#b2c8c1" stroke-width="2.5">
        <path d="M-110 0H110M0-110V110M-78-78 78 78M-78 78 78-78M-102-42 102 42M-102 42 102-42M-42-102 42 102M-42 102 42-102"/>
      </g>
      <circle r="11" fill="#f4ba61" stroke="#304e51" stroke-width="4"/>
    </g>
    <g id="cloud-tile" fill="#fffdf6" opacity=".9">
      <path d="M119 164c-8-22 10-39 29-31 1-32 48-39 59-9 28-10 48 16 35 37Z"/>
      <path d="M703 300c-5-17 9-30 24-24 4-27 41-31 50-7 21-5 35 14 25 29Z"/>
    </g>
    <g id="ground-tile">
      <g fill="none" stroke="#8eafa0" stroke-width="4" stroke-linecap="round">
        <path d="M115 670q-2-34-16-45m16 45q6-27 20-35M858 692q-2-30-13-41m13 41q7-25 20-34"/>
      </g>
      <g fill="#d3be94">
        <ellipse cx="156" cy="709" rx="8" ry="3"/>
        <ellipse cx="812" cy="752" rx="11" ry="3"/>
        <ellipse cx="874" cy="717" rx="6" ry="2"/>
      </g>
      <path d="M50 755h85m193 0h85m193 0h85m193 0h55" stroke="#fff9ea" stroke-width="5" stroke-linecap="round" opacity=".85"/>
    </g>
  </defs>

  <!-- Soft sea air and a sandy coastal path. -->
  <rect width="1000" height="800" rx="36" fill="url(#sky)"/>
  <circle cx="779" cy="147" r="62" fill="#f8d98a" opacity=".75"/>
  <g id="cloud-strip"><use href="#cloud-tile"/><use href="#cloud-tile" x="1000"/></g>
  <path d="M0 496c159-25 257 21 398 1s260-22 397 0 165 6 205-2v125H0Z" fill="#cde4dc"/>
  <path id="sea-wave" d="M0 543c164-32 244 32 407 0s263-12 406 4 147-4 187-2v93H0Z" fill="#b8d8d0" opacity=".65"/>
  <path d="M0 620c223-43 368 19 526 1s316-21 474 17v162H0Z" fill="#f2e5c9"/>
  <path d="M0 685c238-22 379 25 561-2s303-9 439 4" fill="none" stroke="#e5d6b7" stroke-width="4"/>
  <ellipse cx="500" cy="724" rx="360" ry="19" fill="#b7ad91" opacity=".2"/>
  <g id="ground-strip"><use href="#ground-tile"/><use href="#ground-tile" x="1000"/></g>

  <!-- Bicycle: the wheels, far pedal, then the diamond frame. -->
  <g transform="translate(290 590)"><g id="rear-spin"><use href="#wheel"/></g></g>
  <g transform="translate(708 590)"><g id="front-spin"><use href="#wheel"/></g></g>
  <g fill="none" stroke-linecap="round" stroke-linejoin="round">
    <path id="far-crank" d="M478 585 438 562" stroke="#304e51" stroke-width="8"/>
    <g id="far-pedal" transform="translate(438 562)"><path d="M-18 5H18" stroke="#304e51" stroke-width="9"/></g>
    <path id="far-leg" d="M444 401 504 470 438 562" stroke="#b97143" stroke-width="16"/>
    <g id="far-foot" transform="translate(438 562)"><path d="M-12-12 7-14 25-3 29 3-14 3Z" fill="#e7a24d" stroke="#805d43" stroke-width="3"/></g>
    <path d="m290 590 131-160 57 155H290l154-124h182L478 585m148-124 82 129" stroke="#234f50" stroke-width="14"/>
    <path d="m290 590 131-160 57 155H290l154-124h182L478 585m148-124 82 129" stroke="#3c9e95" stroke-width="8"/>
    <path d="m421 430-11-34m216 65-17-60q-7-25 16-27h31" stroke="#304e51" stroke-width="10"/>
    <path d="M639 374h24" stroke="#bd7250" stroke-width="13"/>
    <path d="M623 391q36 34 47 91" stroke="#567673" stroke-width="3"/>
  </g>
  <path d="M376 392q27-13 63-4 10 3 8 12-3 8-20 7h-48q-14-1-11-8 2-5 8-7Z" fill="#875e4c" stroke="#304e51" stroke-width="4"/>
  <path d="M182 530a128 128 0 0 1 206-24M602 514a128 128 0 0 1 203 10" fill="none" stroke="#e9b75c" stroke-width="9" stroke-linecap="round"/>
  <circle cx="478" cy="585" r="25" fill="#f4d291" stroke="#304e51" stroke-width="5"/>
  <circle cx="478" cy="585" r="8" fill="#304e51"/>
  <path id="near-crank" d="M478 585 518 608" stroke="#304e51" stroke-width="8" stroke-linecap="round"/>
  <g id="near-pedal" transform="translate(518 608)"><path d="M-19 5H19" stroke="#304e51" stroke-width="9" stroke-linecap="round"/></g>

  <!-- 鹈鹕身体单独分组，随蹬踏轻轻起伏。 -->
  <g id="rider-body">
  <path d="m360 326-78-29 35 45-51-8 66 49 51-16Z" fill="#f3f4e9" stroke="#365456" stroke-width="5" stroke-linejoin="round"/>

  <!-- Round body, tall curved neck, and a very pelican-shaped head. -->
  <path d="M346 280c33-29 88-22 121-1 18 11 27 27 38 26 13-2 14-17 10-36-7-29-17-48-11-74 6-27 28-43 53-42 33 0 54 23 51 50-2 23-18 37-38 42-5 22 18 57 11 96-6 36-34 65-75 73-38 7-111 2-145-23-42-31-53-79-15-111Z" fill="url(#feathers)" stroke="#365456" stroke-width="5" stroke-linejoin="round"/>
  <path d="M520 206q-4-31 21-40m-6-7-9-17m22 13-1-21" fill="none" stroke="#365456" stroke-width="4" stroke-linecap="round"/>
  <path d="M552 249c2 32 24 62 13 93" fill="none" stroke="#c7d8ce" stroke-width="7" stroke-linecap="round"/>

  <!-- The lower bill stretches into the characteristic hanging pouch. -->
  <path d="M587 197 761 217c-19 14-42 31-68 42-37 17-75 10-89-9-10-14-13-34-17-53Z" fill="url(#pouch)" stroke="#365456" stroke-width="4" stroke-linejoin="round"/>
  <path d="M616 222q18 38 58 29" fill="none" stroke="#f8c29a" stroke-width="5" stroke-linecap="round"/>
  <path d="M588 179c50 3 130 18 185 34 9 3 10 9-1 11l-177-15q-12-12-7-30Z" fill="url(#bill)" stroke="#365456" stroke-width="4" stroke-linejoin="round"/>
  <path d="m604 195 151 22" fill="none" stroke="#da813b" stroke-width="2.5" stroke-linecap="round"/>
  <g id="bird-eye">
  <ellipse cx="578" cy="182" rx="12" ry="14" fill="#e9cb79"/>
  <circle cx="580" cy="181" r="6.5" fill="#273e42"/>
  <circle cx="582" cy="178" r="2" fill="#fff"/>
  </g>
  <path d="M562 164q9-6 19-1" fill="none" stroke="#365456" stroke-width="3" stroke-linecap="round"/>
  <ellipse cx="571" cy="210" rx="10" ry="6" fill="#f1bd9b" opacity=".7"/>

  </g>
  <!-- 近侧腿：轮廓与填色共享同一条动态折线路径。 -->
  <g fill="none" stroke-linecap="round" stroke-linejoin="round">
    <path id="near-leg-outline" d="M465 403 559 480 518 608" stroke="#805d43" stroke-width="20"/>
    <path id="near-leg" d="M465 403 559 480 518 608" stroke="#eba84f" stroke-width="13"/>
  </g>
  <g id="near-foot" transform="translate(518 608)">
    <path d="M-12-12 6-14 21-5 30 2Q31 5 23 5H-13Z" fill="#f1b258" stroke="#805d43" stroke-width="3.5" stroke-linejoin="round"/>
    <path d="M6-5 16 2M-2-3 5 3" fill="none" stroke="#cc8743" stroke-width="2.5" stroke-linecap="round"/>
  </g>
  <!-- The near wing reaches naturally toward the handlebars. -->
  <g id="rider-wing">
  <path d="M367 303c31-14 70-8 101 15 25 19 34 37 58 45 32 11 66-1 89 5 8 2 12 9 5 14-14 9-47 22-78 20-44-3-72-21-102-30-26-7-63-15-73-36" fill="#edf1e7" stroke="#365456" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
  <g fill="none" stroke="#bbcfc4" stroke-width="4" stroke-linecap="round">
    <path d="M388 325q37 1 65 23t62 35"/>
    <path d="M386 341q34 5 60 23"/>
    <path d="M541 386q37 3 61-9"/>
  </g>

  </g>
  <!-- A little breeze and two distant gulls. -->
  <g fill="none" stroke="#7eaaa2" stroke-width="4" stroke-linecap="round">
    <path d="M179 379h72m-92 26h50m-7 25h41"/>
    <path d="M330 153q13-13 25 0 13-13 25 0M817 388q10-11 20 0 10-11 20 0"/>
  </g>
</svg>
      <div class="controls">
        <button id="toggle" type="button" aria-controls="coastal-scene">暂停动画</button>
        <button id="reset" type="button">回到起点</button>
        <label class="speed" for="speed">骑行速度
          <input id="speed" type="range" min="0.5" max="2" step="0.1" value="1">
          <output id="speed-value" for="speed">1.0×</output>
        </label>
      </div>
      <noscript><p>开启 JavaScript，即可观看鹈鹕骑行；当前展示静态插画。</p></noscript>
    </section>
    <footer><span>一只鹈鹕，一辆单车，一整天的海风。</span><p id="status" role="status" aria-live="polite">正在海岸漫游</p></footer>
  </main>
  <script>
    (() => {
      'use strict';
      const byId = id => document.getElementById(id);
      const parts = Object.fromEntries([
        'rear-spin', 'front-spin', 'far-crank', 'near-crank', 'far-pedal',
        'near-pedal', 'far-leg', 'near-leg-outline', 'near-leg', 'far-foot',
        'near-foot', 'rider-body', 'rider-wing', 'ground-strip', 'cloud-strip',
        'sea-wave', 'bird-eye', 'toggle', 'reset', 'speed', 'speed-value', 'status'
      ].map(id => [id, byId(id)]));

      const motionPreference = window.matchMedia('(prefers-reduced-motion: reduce)');
      let playing = !motionPreference.matches;
      let speed = 1;
      let distance = 0;
      let elapsed = 0;
      let previousTime = null;
      let frameId = null;
      const crankCenter = { x: 478, y: 585 };
      const crankRadius = 46;
      const wheelRadius = 126;
      const gearRatio = 2.1;
      const clamp = (n, lo, hi) => Math.max(lo, Math.min(hi, n));

      // 两段式腿部：给定髋部、脚踏和两段腿长，求膝盖坐标。
      function kneePosition(hip, foot, upper, lower) {
        const dx = foot.x - hip.x;
        const dy = foot.y - hip.y;
        const actualDistance = Math.hypot(dx, dy);
        const reach = clamp(actualDistance, Math.abs(upper - lower) + .001, upper + lower - .001);
        const baseAngle = Math.atan2(dy, dx);
        const bend = Math.acos(clamp((upper * upper + reach * reach - lower * lower) / (2 * upper * reach), -1, 1));
        return { x: hip.x + Math.cos(baseAngle - bend) * upper,
                 y: hip.y + Math.sin(baseAngle - bend) * upper };
      }

      function drawLeg(hip, foot, paths, footElement, upper, lower) {
        const knee = kneePosition(hip, foot, upper, lower);
        const d = `M${hip.x},${hip.y} L${knee.x},${knee.y} L${foot.x},${foot.y}`;
        paths.forEach(path => path.setAttribute('d', d));
        // 脚蹼始终大致水平，脚踏不随曲柄一起翻转。
        footElement.setAttribute('transform', `translate(${foot.x} ${foot.y})`);
      }

      function render() {
        const wheelAngle = distance / wheelRadius;
        const pedalAngle = wheelAngle / gearRatio + Math.PI / 6;
        const bob = Math.sin(pedalAngle * 2) * 2;
        const wheelDegrees = wheelAngle * 180 / Math.PI;
        parts['rear-spin'].setAttribute('transform', `rotate(${wheelDegrees})`);
        parts['front-spin'].setAttribute('transform', `rotate(${wheelDegrees})`);
        parts['rider-body'].setAttribute('transform', `translate(0 ${bob})`);
        parts['rider-wing'].setAttribute('transform', `rotate(${bob * .1} 615 375)`);

        const nearFoot = {
          x: crankCenter.x + Math.cos(pedalAngle) * crankRadius,
          y: crankCenter.y + Math.sin(pedalAngle) * crankRadius
        };
        const farFoot = {
          x: crankCenter.x - Math.cos(pedalAngle) * crankRadius,
          y: crankCenter.y - Math.sin(pedalAngle) * crankRadius
        };
        for (const [side, foot] of [['near', nearFoot], ['far', farFoot]]) {
          parts[`${side}-crank`].setAttribute('d', `M478 585 L${foot.x} ${foot.y}`);
          parts[`${side}-pedal`].setAttribute('transform', `translate(${foot.x} ${foot.y})`);
        }
        drawLeg({ x: 444, y: 401 + bob }, farFoot,
          [parts['far-leg']], parts['far-foot'], 120, 124);
        drawLeg({ x: 465, y: 403 + bob }, nearFoot,
          [parts['near-leg-outline'], parts['near-leg']], parts['near-foot'], 120, 124);

        // 每个循环带宽 1000，两个相同的图块首尾相接。
        parts['ground-strip'].setAttribute('transform', `translate(${-distance % 1000} 0)`);
        parts['cloud-strip'].setAttribute('transform', `translate(${-(distance * .13) % 1000} 0)`);
        parts['sea-wave'].setAttribute('transform', `translate(0 ${Math.sin(elapsed * .8) * 3})`);
        const blinkPhase = elapsed % 4.6;
        const eyeScale = blinkPhase > 4.4 ? Math.max(.08, Math.abs(blinkPhase - 4.5) / .1) : 1;
        parts['bird-eye'].setAttribute('transform', `translate(580 181) scale(1 ${eyeScale}) translate(-580 -181)`);
      }

      function tick(now) {
        frameId = null;
        if (!playing || document.hidden) return;
        const delta = previousTime === null ? 0 : Math.min((now - previousTime) / 1000, .05);
        previousTime = now;
        distance += delta * 150 * speed;
        elapsed += delta * speed;
        render();
        frameId = requestAnimationFrame(tick);
      }

      function syncPlayback() {
        if (frameId !== null) cancelAnimationFrame(frameId);
        frameId = null;
        previousTime = null;
        parts.toggle.textContent = playing ? '暂停动画' : '播放动画';
        parts.status.textContent = playing ? '正在海岸漫游' : '已暂停，歇一会儿再出发';
        if (playing && !document.hidden) frameId = requestAnimationFrame(tick);
      }

      parts.toggle.addEventListener('click', () => { playing = !playing; syncPlayback(); });
      parts.reset.addEventListener('click', () => {
        distance = 0;
        elapsed = 0;
        previousTime = null;
        render();
        parts.status.textContent = playing ? '已回到起点，继续骑行' : '已回到起点，动画暂停中';
      });
      parts.speed.addEventListener('input', event => {
        speed = Number(event.target.value);
        parts['speed-value'].value = `${speed.toFixed(1)}×`;
        parts.speed.setAttribute('aria-valuetext', `${speed.toFixed(1)} 倍`);
      });
      // 切回页面时重置时间基准，避免后台停留导致画面跳跃。
      document.addEventListener('visibilitychange', syncPlayback);
      motionPreference.addEventListener('change', event => {
        playing = !event.matches;
        syncPlayback();
      });
      render();
      syncPlayback();
      if (motionPreference.matches) parts.status.textContent = '已按系统的减少动态效果偏好暂停，可手动播放';
    })();
  </script>
</body>
</html>
```

这样，内层执行 `rotate(angle)` 时，旋转中心就是该车轮的局部原点，不需要把整个车轮绕画布原点旋转。

## 3. 用统一的距离驱动车轮和脚踏

动画中保留两个主要状态：`distance` 表示累计骑行距离，`elapsed` 表示累计动画时间。每一帧使用时间差更新状态：

```js
distance += delta * 150 * speed;
elapsed += delta * speed;
```

这里的距离使用 SVG 逻辑单位。`150` 表示基础速度，没有对应真实公里数。`delta` 是两帧之间的秒数，滑块控制 `speed`。

车轮半径为 126，根据弧长关系 `s = rθ`，得到车轮转角：

```js
const wheelAngle = distance / 126;
const pedalAngle = wheelAngle / 2.1 + Math.PI / 6;
```

`2.1` 是画面采用的传动比例：曲柄旋转一圈，车轮旋转约 2.1 圈。初始角度偏移让双脚一开始就处于自然的蹬踏位置。

脚踏沿曲柄中心周围做圆周运动：

```js
const nearFoot = {
  x: 478 + Math.cos(pedalAngle) * 46,
  y: 585 + Math.sin(pedalAngle) * 46
};
const farFoot = {
  x: 478 - Math.cos(pedalAngle) * 46,
  y: 585 - Math.sin(pedalAngle) * 46
};
```

两个脚踏相差半圈。曲柄连接中心与脚踏，脚蹼和踏板的位置也直接使用这两个坐标，避免出现脚与踏板分离的情况。踏板只平移，保持水平。

调速时仅改变每帧新增的距离，已经积累的距离不变，因此动作相位保持连续。

## 4. 用两段式逆运动学计算膝盖

蹬车动画里，脚部轨迹已由脚踏确定，但膝盖位置仍需要计算。把一条腿简化成髋部、膝盖、脚部三个点，并固定上下两段长度，就能用三角形求出膝盖。

设髋部到脚部的距离为 `d`，上段长为 `a`，下段长为 `b`。根据余弦定理：

```text
cos(α) = (a² + d² - b²) / (2ad)
```

再用 `atan2(dy, dx)` 求髋部指向脚部的方向角 `β`，选择朝前弯曲的分支：

```js
const knee = {
  x: hip.x + Math.cos(beta - alpha) * upper,
  y: hip.y + Math.sin(beta - alpha) * upper
};
```

最后更新路径：

```js
const d = `M${hip.x},${hip.y} L${knee.x},${knee.y} L${foot.x},${foot.y}`;
path.setAttribute('d', d);
```

实现中把两段腿长设置为 120 和 124，并对距离和余弦值做范围限制，避免浮点误差使 `acos()` 产生无效值。这里的腿长与髋部位置针对本场景设置；如果大幅改动车架或角色比例，需要重新安排可达范围。

近侧腿使用两条重合路径：粗一些的深色描边作为轮廓，细一些的橙色描边作为腿部颜色。两条路径共享相同的坐标更新。

## 5. 给背景增加视差和无缝循环

自行车保持在画面中央，背景向左移动，就能表现出向右前进。

地面装饰做成宽度为 1000 的图块，用两份相同图块首尾相接。位移达到一个图块宽度后，通过取模回到循环开头：

```js
groundStrip.setAttribute('transform', `translate(${-distance % 1000} 0)`);
cloudStrip.setAttribute('transform', `translate(${-(distance * .13) % 1000} 0)`);
```

地面使用完整速度，云朵只使用 13% 的速度，远景因此显得移动更慢。两份图块在循环边界具有相同布局，重置位移时可以继续衔接。

为使地面运动与车轮一致，车轮转角和地面位移都使用同一个 `distance`。身体用小幅正弦函数起伏，眨眼按动画时间周期缩放眼睛高度。这些细节一起受播放状态控制。

## 6. 管理动画循环与暂停状态

使用 `requestAnimationFrame()` 请求下一帧。动画暂停时取消请求，恢复时清空上一帧时间，让新的时间差从零开始。

```js
const delta = previousTime === null
  ? 0
  : Math.min((now - previousTime) / 1000, .05);
```

单帧时间差限制为 0.05 秒，遇到卡顿时避免一次推进太远；其代价是严重卡顿时动画会比实际经过的时间慢一些。

切换到后台时停止帧循环，返回页面时重新建立时间基准。按钮文字与页面状态提示同步更新，滑块也提供可读的倍速值。画布包含 SVG 的 `<title>` 和 `<desc>`，在没有 JavaScript 时仍保留静态插画。

## 7. 完整 HTML 源码

新建 `pelican-bicycle.html`，复制以下全部代码并保存。无需构建步骤或本地服务器。

```html
<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#f5f3eb">
  <title>海岸漫游 · 鹈鹕骑自行车</title>
  <style>
    :root { color-scheme: light; --ink: #294c4d; --muted: #6a827b; --accent: #2b8278; }
    * { box-sizing: border-box; }
    body { margin: 0; background: #f5f3eb; color: var(--ink); font-family: "Segoe UI", "Microsoft YaHei", sans-serif; }
    main { max-width: 1060px; margin: auto; padding: 42px 28px 24px; }
    header { display: flex; align-items: end; justify-content: space-between; gap: 24px; margin-bottom: 24px; }
    .eyebrow { margin: 0 0 10px; color: var(--accent); font-size: 11px; font-weight: 700; letter-spacing: .23em; }
    h1 { margin: 0; font-size: clamp(26px, 4vw, 40px); font-weight: 600; letter-spacing: .03em; }
    .intro { margin: 0 0 3px; color: var(--muted); line-height: 1.8; font-size: 14px; }
    .scene { overflow: hidden; border: 1px solid #dce4d7; border-radius: 28px; background: #edf7f4; box-shadow: 0 18px 55px #294c4d0c; }
    .scene svg { display: block; width: 100%; height: auto; max-height: 68vh; min-height: 280px; }
    .controls { display: flex; align-items: center; flex-wrap: wrap; gap: 14px 20px; padding: 18px 24px; background: #fffdf5; border-top: 1px solid #e0e8da; }
    button { cursor: pointer; font: inherit; border: 0; border-radius: 24px; padding: 11px 20px; font-size: 14px; }
    #toggle { min-width: 108px; color: #fffdf5; background: var(--accent); }
    #reset { color: var(--ink); background: #eaf0e5; }
    button:hover { filter: brightness(.95); }
    button:focus-visible, input:focus-visible { outline: 3px solid #d5903e; outline-offset: 4px; }
    .speed { display: flex; align-items: center; gap: 12px; margin-left: auto; font-size: 13px; }
    input[type="range"] { width: clamp(95px, 15vw, 170px); accent-color: var(--accent); cursor: pointer; }
    output { width: 3.5em; font-variant-numeric: tabular-nums; }
    footer { display: flex; justify-content: space-between; flex-wrap: wrap; gap: 8px; padding: 18px 3px 0; font-size: 12px; color: var(--muted); }
    #status { margin: 0; }
    noscript p { padding: 0 24px 16px; color: var(--muted); }
    @media (max-width: 640px) {
      main { padding: 24px 14px; }
      header { display: block; }
      .intro { margin-top: 12px; }
      .scene { border-radius: 20px; }
      .controls { padding: 16px; gap: 12px; }
      .speed { margin-left: 0; width: 100%; }
      input[type="range"] { flex: 1; }
    }
  </style>
</head>
<body>
  <main>
    <header>
      <div><p class="eyebrow">PELICAN RIDING CLUB / 01</p><h1>海风正好，骑慢一点。</h1></div>
      <p class="intro">跟着鹈鹕，沿海岸兜个风。<br>今天的目的地，是好心情。</p>
    </header>
    <section class="scene" aria-label="鹈鹕的海边骑行">
<svg id="coastal-scene" xmlns="http://www.w3.org/2000/svg" width="1000" height="800" viewBox="0 0 1000 800" role="img" aria-labelledby="title description">
  <title id="title">鹈鹕骑自行车</title>
  <desc id="description">一只长着橙色大嘴的白色鹈鹕，骑着青绿色自行车，双腿交替蹬踏，车轮转动，云朵与海边小路向后移动。</desc>
  <defs>
    <linearGradient id="sky" x2="0" y2="1">
      <stop stop-color="#edf7f4"/>
      <stop offset="1" stop-color="#fff8e9"/>
    </linearGradient>
    <linearGradient id="feathers" x1="0" y1="0" x2=".8" y2="1">
      <stop stop-color="#fffef8"/>
      <stop offset="1" stop-color="#e0e9e2"/>
    </linearGradient>
    <linearGradient id="bill" x2="0" y2="1">
      <stop stop-color="#ffc65e"/>
      <stop offset="1" stop-color="#f49a42"/>
    </linearGradient>
    <linearGradient id="pouch" x2="0" y2="1">
      <stop stop-color="#f7b17a"/>
      <stop offset="1" stop-color="#e98a69"/>
    </linearGradient>
    <g id="wheel">
      <circle r="126" fill="#fffaf0" stroke="#304e51" stroke-width="15"/>
      <circle r="113" fill="none" stroke="#c4d3c9" stroke-width="3"/>
      <g stroke="#b2c8c1" stroke-width="2.5">
        <path d="M-110 0H110M0-110V110M-78-78 78 78M-78 78 78-78M-102-42 102 42M-102 42 102-42M-42-102 42 102M-42 102 42-102"/>
      </g>
      <circle r="11" fill="#f4ba61" stroke="#304e51" stroke-width="4"/>
    </g>
    <g id="cloud-tile" fill="#fffdf6" opacity=".9">
      <path d="M119 164c-8-22 10-39 29-31 1-32 48-39 59-9 28-10 48 16 35 37Z"/>
      <path d="M703 300c-5-17 9-30 24-24 4-27 41-31 50-7 21-5 35 14 25 29Z"/>
    </g>
    <g id="ground-tile">
      <g id="ground-strip"><use href="#ground-tile"/><use href="#ground-tile" x="1000"/></g>
      <path d="M50 755h85m193 0h85m193 0h85m193 0h55" stroke="#fff9ea" stroke-width="5" stroke-linecap="round" opacity=".85"/>
    </g>
  </defs>

  <!-- Soft sea air and a sandy coastal path. -->
  <rect width="1000" height="800" rx="36" fill="url(#sky)"/>
  <circle cx="779" cy="147" r="62" fill="#f8d98a" opacity=".75"/>
  <g id="cloud-strip"><use href="#cloud-tile"/><use href="#cloud-tile" x="1000"/></g>
  <path d="M0 496c159-25 257 21 398 1s260-22 397 0 165 6 205-2v125H0Z" fill="#cde4dc"/>
  <path id="sea-wave" d="M0 543c164-32 244 32 407 0s263-12 406 4 147-4 187-2v93H0Z" fill="#b8d8d0" opacity=".65"/>
  <path d="M0 620c223-43 368 19 526 1s316-21 474 17v162H0Z" fill="#f2e5c9"/>
  <path d="M0 685c238-22 379 25 561-2s303-9 439 4" fill="none" stroke="#e5d6b7" stroke-width="4"/>
  <ellipse cx="500" cy="724" rx="360" ry="19" fill="#b7ad91" opacity=".2"/>
  <g id="ground-strip"><use href="#ground-tile"/><use href="#ground-tile" x="1000"/></g>

  <!-- Bicycle: the wheels, far pedal, then the diamond frame. -->
  <g transform="translate(290 590)"><g id="rear-spin"><use href="#wheel"/></g></g>
  <g transform="translate(708 590)"><g id="front-spin"><use href="#wheel"/></g></g>
  <g fill="none" stroke-linecap="round" stroke-linejoin="round">
    <path id="far-crank" d="M478 585 438 562" stroke="#304e51" stroke-width="8"/>
    <g id="far-pedal" transform="translate(438 562)"><path d="M-18 5H18" stroke="#304e51" stroke-width="9"/></g>
    <path id="far-leg" d="M444 401 504 470 438 562" stroke="#b97143" stroke-width="16"/>
    <g id="far-foot" transform="translate(438 562)"><path d="M-12-12 7-14 25-3 29 3-14 3Z" fill="#e7a24d" stroke="#805d43" stroke-width="3"/></g>
    <path d="m290 590 131-160 57 155H290l154-124h182L478 585m148-124 82 129" stroke="#234f50" stroke-width="14"/>
    <path d="m290 590 131-160 57 155H290l154-124h182L478 585m148-124 82 129" stroke="#3c9e95" stroke-width="8"/>
    <path d="m421 430-11-34m216 65-17-60q-7-25 16-27h31" stroke="#304e51" stroke-width="10"/>
    <path d="M639 374h24" stroke="#bd7250" stroke-width="13"/>
    <path d="M623 391q36 34 47 91" stroke="#567673" stroke-width="3"/>
  </g>
  <path d="M376 392q27-13 63-4 10 3 8 12-3 8-20 7h-48q-14-1-11-8 2-5 8-7Z" fill="#875e4c" stroke="#304e51" stroke-width="4"/>
  <path d="M182 530a128 128 0 0 1 206-24M602 514a128 128 0 0 1 203 10" fill="none" stroke="#e9b75c" stroke-width="9" stroke-linecap="round"/>
  <circle cx="478" cy="585" r="25" fill="#f4d291" stroke="#304e51" stroke-width="5"/>
  <circle cx="478" cy="585" r="8" fill="#304e51"/>
  <path id="near-crank" d="M478 585 518 608" stroke="#304e51" stroke-width="8" stroke-linecap="round"/>
  <g id="near-pedal" transform="translate(518 608)"><path d="M-19 5H19" stroke="#304e51" stroke-width="9" stroke-linecap="round"/></g>

  <!-- 鹈鹕身体单独分组，随蹬踏轻轻起伏。 -->
  <g id="rider-body">
  <path d="m360 326-78-29 35 45-51-8 66 49 51-16Z" fill="#f3f4e9" stroke="#365456" stroke-width="5" stroke-linejoin="round"/>

  <!-- Round body, tall curved neck, and a very pelican-shaped head. -->
  <path d="M346 280c33-29 88-22 121-1 18 11 27 27 38 26 13-2 14-17 10-36-7-29-17-48-11-74 6-27 28-43 53-42 33 0 54 23 51 50-2 23-18 37-38 42-5 22 18 57 11 96-6 36-34 65-75 73-38 7-111 2-145-23-42-31-53-79-15-111Z" fill="url(#feathers)" stroke="#365456" stroke-width="5" stroke-linejoin="round"/>
  <path d="M520 206q-4-31 21-40m-6-7-9-17m22 13-1-21" fill="none" stroke="#365456" stroke-width="4" stroke-linecap="round"/>
  <path d="M552 249c2 32 24 62 13 93" fill="none" stroke="#c7d8ce" stroke-width="7" stroke-linecap="round"/>

  <!-- The lower bill stretches into the characteristic hanging pouch. -->
  <path d="M587 197 761 217c-19 14-42 31-68 42-37 17-75 10-89-9-10-14-13-34-17-53Z" fill="url(#pouch)" stroke="#365456" stroke-width="4" stroke-linejoin="round"/>
  <path d="M616 222q18 38 58 29" fill="none" stroke="#f8c29a" stroke-width="5" stroke-linecap="round"/>
  <path d="M588 179c50 3 130 18 185 34 9 3 10 9-1 11l-177-15q-12-12-7-30Z" fill="url(#bill)" stroke="#365456" stroke-width="4" stroke-linejoin="round"/>
  <path d="m604 195 151 22" fill="none" stroke="#da813b" stroke-width="2.5" stroke-linecap="round"/>
  <g id="bird-eye">
  <ellipse cx="578" cy="182" rx="12" ry="14" fill="#e9cb79"/>
  <circle cx="580" cy="181" r="6.5" fill="#273e42"/>
  <circle cx="582" cy="178" r="2" fill="#fff"/>
  </g>
  <path d="M562 164q9-6 19-1" fill="none" stroke="#365456" stroke-width="3" stroke-linecap="round"/>
  <ellipse cx="571" cy="210" rx="10" ry="6" fill="#f1bd9b" opacity=".7"/>

  </g>
  <!-- 近侧腿：轮廓与填色共享同一条动态折线路径。 -->
  <g fill="none" stroke-linecap="round" stroke-linejoin="round">
    <path id="near-leg-outline" d="M465 403 559 480 518 608" stroke="#805d43" stroke-width="20"/>
    <path id="near-leg" d="M465 403 559 480 518 608" stroke="#eba84f" stroke-width="13"/>
  </g>
  <g id="near-foot" transform="translate(518 608)">
    <path d="M-12-12 6-14 21-5 30 2Q31 5 23 5H-13Z" fill="#f1b258" stroke="#805d43" stroke-width="3.5" stroke-linejoin="round"/>
    <path d="M6-5 16 2M-2-3 5 3" fill="none" stroke="#cc8743" stroke-width="2.5" stroke-linecap="round"/>
  </g>
  <!-- The near wing reaches naturally toward the handlebars. -->
  <g id="rider-wing">
  <path d="M367 303c31-14 70-8 101 15 25 19 34 37 58 45 32 11 66-1 89 5 8 2 12 9 5 14-14 9-47 22-78 20-44-3-72-21-102-30-26-7-63-15-73-36" fill="#edf1e7" stroke="#365456" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
  <g fill="none" stroke="#bbcfc4" stroke-width="4" stroke-linecap="round">
    <path d="M388 325q37 1 65 23t62 35"/>
    <path d="M386 341q34 5 60 23"/>
    <path d="M541 386q37 3 61-9"/>
  </g>

  </g>
  <!-- A little breeze and two distant gulls. -->
  <g fill="none" stroke="#7eaaa2" stroke-width="4" stroke-linecap="round">
    <path d="M179 379h72m-92 26h50m-7 25h41"/>
    <path d="M330 153q13-13 25 0 13-13 25 0M817 388q10-11 20 0 10-11 20 0"/>
  </g>
</svg>
      <div class="controls">
        <button id="toggle" type="button" aria-controls="coastal-scene">暂停动画</button>
        <button id="reset" type="button">回到起点</button>
        <label class="speed" for="speed">骑行速度
          <input id="speed" type="range" min="0.5" max="2" step="0.1" value="1">
          <output id="speed-value" for="speed">1.0×</output>
        </label>
      </div>
      <noscript><p>开启 JavaScript，即可观看鹈鹕骑行；当前展示静态插画。</p></noscript>
    </section>
    <footer><span>一只鹈鹕，一辆单车，一整天的海风。</span><p id="status" role="status" aria-live="polite">正在海岸漫游</p></footer>
  </main>
  <script>
    (() => {
      'use strict';
      const byId = id => document.getElementById(id);
      const parts = Object.fromEntries([
        'rear-spin', 'front-spin', 'far-crank', 'near-crank', 'far-pedal',
        'near-pedal', 'far-leg', 'near-leg-outline', 'near-leg', 'far-foot',
        'near-foot', 'rider-body', 'rider-wing', 'ground-strip', 'cloud-strip',
        'sea-wave', 'bird-eye', 'toggle', 'reset', 'speed', 'speed-value', 'status'
      ].map(id => [id, byId(id)]));

      const motionPreference = window.matchMedia('(prefers-reduced-motion: reduce)');
      let playing = !motionPreference.matches;
      let speed = 1;
      let distance = 0;
      let elapsed = 0;
      let previousTime = null;
      let frameId = null;
      const crankCenter = { x: 478, y: 585 };
      const crankRadius = 46;
      const wheelRadius = 126;
      const gearRatio = 2.1;
      const clamp = (n, lo, hi) => Math.max(lo, Math.min(hi, n));

      // 两段式腿部：给定髋部、脚踏和两段腿长，求膝盖坐标。
      function kneePosition(hip, foot, upper, lower) {
        const dx = foot.x - hip.x;
        const dy = foot.y - hip.y;
        const actualDistance = Math.hypot(dx, dy);
        const reach = clamp(actualDistance, Math.abs(upper - lower) + .001, upper + lower - .001);
        const baseAngle = Math.atan2(dy, dx);
        const bend = Math.acos(clamp((upper * upper + reach * reach - lower * lower) / (2 * upper * reach), -1, 1));
        return { x: hip.x + Math.cos(baseAngle - bend) * upper,
                 y: hip.y + Math.sin(baseAngle - bend) * upper };
      }

      function drawLeg(hip, foot, paths, footElement, upper, lower) {
        const knee = kneePosition(hip, foot, upper, lower);
        const d = `M${hip.x},${hip.y} L${knee.x},${knee.y} L${foot.x},${foot.y}`;
        paths.forEach(path => path.setAttribute('d', d));
        // 脚蹼始终大致水平，脚踏不随曲柄一起翻转。
        footElement.setAttribute('transform', `translate(${foot.x} ${foot.y})`);
      }

      function render() {
        const wheelAngle = distance / wheelRadius;
        const pedalAngle = wheelAngle / gearRatio + Math.PI / 6;
        const bob = Math.sin(pedalAngle * 2) * 2;
        const wheelDegrees = wheelAngle * 180 / Math.PI;
        parts['rear-spin'].setAttribute('transform', `rotate(${wheelDegrees})`);
        parts['front-spin'].setAttribute('transform', `rotate(${wheelDegrees})`);
        parts['rider-body'].setAttribute('transform', `translate(0 ${bob})`);
        parts['rider-wing'].setAttribute('transform', `rotate(${bob * .1} 615 375)`);

        const nearFoot = {
          x: crankCenter.x + Math.cos(pedalAngle) * crankRadius,
          y: crankCenter.y + Math.sin(pedalAngle) * crankRadius
        };
        const farFoot = {
          x: crankCenter.x - Math.cos(pedalAngle) * crankRadius,
          y: crankCenter.y - Math.sin(pedalAngle) * crankRadius
        };
        for (const [side, foot] of [['near', nearFoot], ['far', farFoot]]) {
          parts[`${side}-crank`].setAttribute('d', `M478 585 L${foot.x} ${foot.y}`);
          parts[`${side}-pedal`].setAttribute('transform', `translate(${foot.x} ${foot.y})`);
        }
        drawLeg({ x: 444, y: 401 + bob }, farFoot,
          [parts['far-leg']], parts['far-foot'], 113, 116);
        drawLeg({ x: 465, y: 403 + bob }, nearFoot,
          [parts['near-leg-outline'], parts['near-leg']], parts['near-foot'], 113, 116);

        // 每个循环带宽 1000，两个相同的图块首尾相接。
        parts['ground-strip'].setAttribute('transform', `translate(${-distance % 1000} 0)`);
        parts['cloud-strip'].setAttribute('transform', `translate(${-(distance * .13) % 1000} 0)`);
        parts['sea-wave'].setAttribute('transform', `translate(0 ${Math.sin(elapsed * .8) * 3})`);
        const blinkPhase = elapsed % 4.6;
        const eyeScale = blinkPhase > 4.4 ? Math.max(.08, Math.abs(blinkPhase - 4.5) / .1) : 1;
        parts['bird-eye'].setAttribute('transform', `translate(580 181) scale(1 ${eyeScale}) translate(-580 -181)`);
      }

      function tick(now) {
        frameId = null;
        if (!playing || document.hidden) return;
        const delta = previousTime === null ? 0 : Math.min((now - previousTime) / 1000, .05);
        previousTime = now;
        distance += delta * 150 * speed;
        elapsed += delta * speed;
        render();
        frameId = requestAnimationFrame(tick);
      }

      function syncPlayback() {
        if (frameId !== null) cancelAnimationFrame(frameId);
        frameId = null;
        previousTime = null;
        parts.toggle.textContent = playing ? '暂停动画' : '播放动画';
        parts.status.textContent = playing ? '正在海岸漫游' : '已暂停，歇一会儿再出发';
        if (playing && !document.hidden) frameId = requestAnimationFrame(tick);
      }

      parts.toggle.addEventListener('click', () => { playing = !playing; syncPlayback(); });
      parts.reset.addEventListener('click', () => {
        distance = 0;
        elapsed = 0;
        previousTime = null;
        render();
        parts.status.textContent = playing ? '已回到起点，继续骑行' : '已回到起点，动画暂停中';
      });
      parts.speed.addEventListener('input', event => {
        speed = Number(event.target.value);
        parts['speed-value'].value = `${speed.toFixed(1)}×`;
        parts.speed.setAttribute('aria-valuetext', `${speed.toFixed(1)} 倍`);
      });
      // 切回页面时重置时间基准，避免后台停留导致画面跳跃。
      document.addEventListener('visibilitychange', syncPlayback);
      motionPreference.addEventListener('change', event => {
        playing = !event.matches;
        syncPlayback();
      });
      render();
      syncPlayback();
      if (motionPreference.matches) parts.status.textContent = '已按系统的减少动态效果偏好暂停，可手动播放';
    })();
  </script>
</body>
</html>
```

## 8. 可以怎样继续修改

| 想调整的效果 | 对应位置 |
| --- | --- |
| 自行车和鹈鹕的配色 | SVG 的 `fill`、`stroke` 与渐变 |
| 默认骑行速度 | `delta * 150 * speed` 中的 `150` |
| 蹬踏频率 | `gearRatio` |
| 曲柄长度 | `crankRadius` |
| 腿长与膝盖弯曲幅度 | `drawLeg()` 传入的上下段长度 |
| 身体起伏幅度 | `Math.sin(pedalAngle * 2) * 2` |
| 远景移动速度 | 云朵位移中的 `.13` |
| 眨眼间隔 | `elapsed % 4.6` |

本例交付为单文件 HTML，所需样式、SVG 和脚本均已内联。本文记录实现过程，按需求未运行自动化测试或浏览器测试。
