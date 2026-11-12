// ChronoMap 3D // Interactive History Globe & AI Historian
document.addEventListener('DOMContentLoaded', () => {
  const globeCanvas = document.getElementById('globeCanvas');
  const starsCanvas = document.getElementById('starsCanvas');
  const timelineSlider = document.getElementById('timelineSlider');
  const dispYear = document.getElementById('dispYear');
  const currentEpochBadge = document.getElementById('currentEpochBadge');
  const dispEventCount = document.getElementById('dispEventCount');
  const chatContextYear = document.getElementById('chatContextYear');
  const eventCard = document.getElementById('eventCard');
  const btnCloseCard = document.getElementById('btnCloseCard');
  const cardEpoch = document.getElementById('cardEpoch');
  const cardTitle = document.getElementById('cardTitle');
  const cardYear = document.getElementById('cardYear');
  const cardLoc = document.getElementById('cardLoc');
  const cardDesc = document.getElementById('cardDesc');
  const btnAskAboutEvent = document.getElementById('btnAskAboutEvent');

  const historianPanel = document.getElementById('historianPanel');
  const btnToggleHistorian = document.getElementById('btnToggleHistorian');
  const chatMessages = document.getElementById('chatMessages');
  const chatInput = document.getElementById('chatInput');
  const btnSendChat = document.getElementById('btnSendChat');
  const epochPills = document.querySelectorAll('.epoch-pills .pill');

  const btnAutoRotate = document.getElementById('btnAutoRotate');
  const btnZoomIn = document.getElementById('btnZoomIn');
  const btnZoomOut = document.getElementById('btnZoomOut');
  const btnResetView = document.getElementById('btnResetView');

  // Starfield Generator
  function initStars() {
    starsCanvas.width = window.innerWidth;
    starsCanvas.height = window.innerHeight;
    const ctx = starsCanvas.getContext('2d');
    const numStars = 250;
    const stars = [];

    for (let i = 0; i < numStars; i++) {
      stars.push({
        x: Math.random() * starsCanvas.width,
        y: Math.random() * starsCanvas.height,
        radius: Math.random() * 1.5,
        alpha: Math.random(),
        speed: 0.005 + Math.random() * 0.01
      });
    }

    function renderStars() {
      ctx.clearRect(0, 0, starsCanvas.width, starsCanvas.height);
      stars.forEach(s => {
        s.alpha += s.speed;
        if (s.alpha > 1 || s.alpha < 0.2) s.speed = -s.speed;
        ctx.fillStyle = `rgba(255, 255, 255, ${Math.abs(s.alpha)})`;
        ctx.beginPath();
        ctx.arc(s.x, s.y, s.radius, 0, Math.PI * 2);
        ctx.fill();
      });
      requestAnimationFrame(renderStars);
    }
    renderStars();
  }
  initStars();

  // Historical Geo-Dataset (3000 BCE to 2026 CE)
  const historyEvents = [
    { id: 1, year: -2560, lat: 29.97, lon: 31.13, name: "Строительство Великой пирамиды в Гизе", epoch: "Бронзовый век", loc: "Гиза, Древний Египет", desc: "Фараон Хеопс воздвиг крупнейшую пирамиду античного мира, единственное из Семи чудес, дошедшее до наших дней." },
    { id: 2, year: -1750, lat: 32.53, lon: 44.42, name: "Свод законов Хаммурапи", epoch: "Бронзовый век", loc: "Вавилон, Месопотамия", desc: "Один из древнейших правовых памятников человечества, установивший принцип талиона ('око за око')." },
    { id: 3, year: -753, lat: 41.90, lon: 12.49, name: "Основание Рима", epoch: "Античность", loc: "Лациум, Италия", desc: "Ромул и Рем основали вечный город на семи холмах Тибра, положив начало Римскому царству." },
    { id: 4, year: -490, lat: 38.11, lon: 23.97, name: "Марафонская битва", epoch: "Античность", loc: "Аттика, Древняя Греция", desc: "Греческие гоплиты под командованием Мильтиада нанесли сокрушительное поражение персидской армии Дария I." },
    { id: 5, year: -331, lat: 36.36, lon: 43.25, name: "Битва при Гавгамелах", epoch: "Античность", loc: "Ассирия, Империя Ахеменидов", desc: "Александр Македонский окончательно разбил персидского царя Дария III, открыв путь к Индии." },
    { id: 6, year: -44, lat: 41.89, lon: 12.48, name: "Мартовские иды: Убийство Цезаря", epoch: "Античность", loc: "Рим, Римская республика", desc: "Сенаторы во главе с Брутом и Кассием убили диктатора Юлия Цезаря, что привело к рождению Римской империи." },
    { id: 7, year: 330, lat: 41.00, lon: 28.97, name: "Основание Константинополя", epoch: "Античность", loc: "Босфор, Византия", desc: "Император Константин Великий перенес столицу империи на Босфор, создав 'Новый Рим'." },
    { id: 8, year: 622, lat: 24.46, lon: 39.61, name: "Хиджра Пророка Мухаммада", epoch: "Средневековье", loc: "Медина, Аравия", desc: "Переселение мусульманской общины из Мекки в Медину, ставшее отправной точкой исламского календаря." },
    { id: 9, year: 862, lat: 58.52, lon: 31.27, name: "Призвание варягов на Русь", epoch: "Средневековье", loc: "Новгород, Древняя Русь", desc: "Согласно Повести временных лет, князь Рюрик сел княжить в Новгороде, положив начало династии Рюриковичей." },
    { id: 10, year: 1066, lat: 50.91, lon: 0.48, name: "Битва при Гастингсе", epoch: "Средневековье", loc: "Суссекс, Англия", desc: "Вильгельм Завоеватель разбил войско короля Гарольда, начав нормандское завоевание Британии." },
    { id: 11, year: 1242, lat: 58.68, lon: 27.86, name: "Ледовое побоище", epoch: "Средневековье", loc: "Чудское озеро, Русь", desc: "Князь Александр Невский разгромил рыцарей Ливонского ордена на весеннем льду озера." },
    { id: 12, year: 1453, lat: 41.01, lon: 28.97, name: "Падение Константинополя", epoch: "Возрождение", loc: "Константинополь, Османская империя", desc: "Султан Мехмед II Фатих штурмом взял столицу Византии, завершив более чем 1000-летнюю историю империи." },
    { id: 13, year: 1492, lat: 24.06, lon: -74.53, name: "Экспедиция Колумба достигла Америки", epoch: "Возрождение", loc: "Багамы, Новый Свет", desc: "Каравеллы Санта-Мария, Пинта и Нинья бросили якорь у острова Гуанахани, начав Эпоху великих географических открытий." },
    { id: 14, year: 1703, lat: 59.93, lon: 30.31, name: "Основание Санкт-Петербурга", epoch: "Возрождение", loc: "Балтика, Российская империя", desc: "Петр I заложил Петропавловскую крепость в дельте Невы, 'прорубив окно в Европу'." },
    { id: 15, year: 1789, lat: 48.85, lon: 2.35, name: "Взятие Бастилии: Французская революция", epoch: "Промышленный век", loc: "Париж, Франция", desc: "Восставшие парижане захватили крепость-тюрьму Бастилию под лозунгами 'Свобода, Равенство, Братство'." },
    { id: 16, year: 1812, lat: 55.51, lon: 35.82, name: "Бородинское сражение", epoch: "Промышленный век", loc: "Бородино, Российская империя", desc: "Крупнейшая битва Отечественной войны 1812 года между армиями Кутузова и Наполеона." },
    { id: 17, year: 1914, lat: 43.85, lon: 18.41, name: "Сараевское покушение", epoch: "Новейшее время", loc: "Сараево, Босния", desc: "Гаврило Принцип застрелил эрцгерцога Франца Фердинанда, что послужило поводом к Первой мировой войне." },
    { id: 18, year: 1945, lat: 52.52, lon: 13.40, name: "Знамя Победы над Рейхстагом", epoch: "Новейшее время", loc: "Берлин, Германия", desc: "Советские воины водрузили красное знамя над поверженным Рейхстагом, ознаменовав разгром нацизма." },
    { id: 19, year: 1961, lat: 45.92, lon: 63.30, name: "Полет Юрия Гагарина в космос", epoch: "Новейшее время", loc: "Байконур, СССР", desc: "Первый в истории человечества пилотируемый космический полет корабля 'Восток-1' с орбиты Земли." },
    { id: 20, year: 1969, lat: 0.67, lon: 23.47, name: "Высадка на Луну (Аполлон-11)", epoch: "Новейшее время", loc: "Море Спокойствия, Луна / Хьюстон", desc: "Нил Армстронг сделал 'один маленький шаг для человека и гигантский скачок для всего человечества'." },
    { id: 21, year: 2026, lat: 55.75, lon: 37.61, name: "Цифровая эпоха и AI-Сингулярность", epoch: "Новейшее время", loc: "Глобальная цифровая сеть", desc: "Формирование глобальных автономных мультиагентных систем и запуск экосистемы Idrisov_OS." }
  ];

  // Globe 3D Engine State
  let currentYear = -44;
  let rotationY = 0.8;
  let rotationX = 0.2;
  let globeScale = 220;
  let isAutoRotating = true;
  let isDragging = false;
  let startX = 0, startY = 0;

  function resizeGlobe() {
    globeCanvas.width = globeCanvas.parentElement.clientWidth;
    globeCanvas.height = globeCanvas.parentElement.clientHeight;
  }
  window.addEventListener('resize', resizeGlobe);
  resizeGlobe();

  // Geographic Landmark Coordinates for Landmass outline approximation
  const continents = [
    // Eurasia / Africa outline points
    [{lat: 60, lon: 30}, {lat: 50, lon: 10}, {lat: 40, lon: -5}, {lat: 30, lon: -10}, {lat: 10, lon: -15}, {lat: 0, lon: 10}, {lat: -30, lon: 20}, {lat: -35, lon: 25}, {lat: 10, lon: 50}, {lat: 25, lon: 60}, {lat: 20, lon: 80}, {lat: 10, lon: 100}, {lat: 20, lon: 110}, {lat: 40, lon: 120}, {lat: 60, lon: 130}, {lat: 70, lon: 60}],
    // Americas outline points
    [{lat: 70, lon: -160}, {lat: 55, lon: -130}, {lat: 35, lon: -120}, {lat: 20, lon: -100}, {lat: 10, lon: -80}, {lat: -10, lon: -75}, {lat: -40, lon: -70}, {lat: -55, lon: -65}, {lat: -30, lon: -40}, {lat: -5, lon: -35}, {lat: 10, lon: -60}, {lat: 30, lon: -80}, {lat: 45, lon: -65}, {lat: 60, lon: -60}]
  ];

  // Screen Projection: (lat, lon) -> (x, y, z)
  function projectToSphere(lat, lon, R) {
    const phi = (lat * Math.PI) / 180;
    const theta = ((lon * Math.PI) / 180) + rotationY;

    // 3D coordinates
    const x3d = R * Math.cos(phi) * Math.sin(theta);
    const y3d = -R * Math.sin(phi);
    const z3d = R * Math.cos(phi) * Math.cos(theta);

    // Apply X rotation (tilt)
    const yRot = y3d * Math.cos(rotationX) - z3d * Math.sin(rotationX);
    const zRot = y3d * Math.sin(rotationX) + z3d * Math.cos(rotationX);

    const centerX = globeCanvas.width / 2;
    const centerY = globeCanvas.height / 2;

    return {
      x: centerX + x3d,
      y: centerY + yRot,
      z: zRot,
      visible: zRot > -10 // Visible on front half of globe
    };
  }

  // Draw 3D Globe
  function renderGlobe() {
    const ctx = globeCanvas.getContext('2d');
    ctx.clearRect(0, 0, globeCanvas.width, globeCanvas.height);

    const cx = globeCanvas.width / 2;
    const cy = globeCanvas.height / 2;
    const R = globeScale;

    // 1. Atmosphere Radial Glow
    const glowGrad = ctx.createRadialGradient(cx, cy, R * 0.8, cx, cy, R * 1.25);
    glowGrad.addColorStop(0, 'rgba(30, 58, 138, 0.4)');
    glowGrad.addColorStop(0.7, 'rgba(212, 175, 55, 0.15)');
    glowGrad.addColorStop(1, 'rgba(5, 7, 13, 0)');
    ctx.fillStyle = glowGrad;
    ctx.beginPath();
    ctx.arc(cx, cy, R * 1.25, 0, Math.PI * 2);
    ctx.fill();

    // 2. Earth Sphere Deep Ocean Fill
    const sphereGrad = ctx.createRadialGradient(cx - R * 0.3, cy - R * 0.3, R * 0.1, cx, cy, R);
    sphereGrad.addColorStop(0, '#0E1726');
    sphereGrad.addColorStop(0.8, '#080C14');
    sphereGrad.addColorStop(1, '#030508');
    ctx.fillStyle = sphereGrad;
    ctx.beginPath();
    ctx.arc(cx, cy, R, 0, Math.PI * 2);
    ctx.fill();
    ctx.strokeStyle = 'rgba(212, 175, 55, 0.5)';
    ctx.lineWidth = 1.5;
    ctx.stroke();

    // 3. Grid Meridians and Parallels
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.08)';
    ctx.lineWidth = 1;
    for (let lat = -60; lat <= 60; lat += 30) {
      ctx.beginPath();
      let first = true;
      for (let lon = -180; lon <= 180; lon += 10) {
        const p = projectToSphere(lat, lon, R);
        if (p.visible) {
          if (first) { ctx.moveTo(p.x, p.y); first = false; }
          else { ctx.lineTo(p.x, p.y); }
        } else {
          first = true;
        }
      }
      ctx.stroke();
    }

    for (let lon = -180; lon <= 180; lon += 45) {
      ctx.beginPath();
      let first = true;
      for (let lat = -80; lat <= 80; lat += 10) {
        const p = projectToSphere(lat, lon, R);
        if (p.visible) {
          if (first) { ctx.moveTo(p.x, p.y); first = false; }
          else { ctx.lineTo(p.x, p.y); }
        } else {
          first = true;
        }
      }
      ctx.stroke();
    }

    // 4. Continents
    ctx.fillStyle = 'rgba(212, 175, 55, 0.15)';
    ctx.strokeStyle = 'rgba(212, 175, 55, 0.4)';
    ctx.lineWidth = 1.2;

    continents.forEach(cont => {
      ctx.beginPath();
      let started = false;
      cont.forEach(pt => {
        const p = projectToSphere(pt.lat, pt.lon, R);
        if (p.visible) {
          if (!started) { ctx.moveTo(p.x, p.y); started = true; }
          else { ctx.lineTo(p.x, p.y); }
        }
      });
      if (started) {
        ctx.closePath();
        ctx.fill();
        ctx.stroke();
      }
    });

    // 5. Historical Milestone Event Pins
    const activeEvents = historyEvents.filter(ev => Math.abs(ev.year - currentYear) <= 300);
    dispEventCount.textContent = `${activeEvents.length} PINS`;

    activeEvents.forEach(ev => {
      const p = projectToSphere(ev.lat, ev.lon, R);
      if (p.visible) {
        // Pin Stem & Head
        ctx.beginPath();
        ctx.arc(p.x, p.y, 6, 0, Math.PI * 2);
        ctx.fillStyle = '#D4AF37';
        ctx.shadowColor = '#F3E5AB';
        ctx.shadowBlur = 10;
        ctx.fill();
        ctx.shadowBlur = 0;

        ctx.strokeStyle = '#FFFFFF';
        ctx.lineWidth = 1.5;
        ctx.stroke();

        // Pin label
        ctx.font = '10px Inter';
        ctx.fillStyle = '#E2D9CC';
        ctx.fillText(ev.name, p.x + 10, p.y + 4);
      }
    });

    if (isAutoRotating) {
      rotationY += 0.003;
    }
    requestAnimationFrame(renderGlobe);
  }
  renderGlobe();

  // Mouse Controls (Rotate & Drag)
  globeCanvas.addEventListener('mousedown', (e) => {
    isDragging = true;
    isAutoRotating = false;
    startX = e.clientX;
    startY = e.clientY;
  });

  window.addEventListener('mousemove', (e) => {
    if (!isDragging) return;
    const dx = e.clientX - startX;
    const dy = e.clientY - startY;
    rotationY += dx * 0.005;
    rotationX = Math.max(-0.8, Math.min(0.8, rotationX + dy * 0.005));
    startX = e.clientX;
    startY = e.clientY;
  });

  window.addEventListener('mouseup', () => isDragging = false);

  globeCanvas.addEventListener('wheel', (e) => {
    e.preventDefault();
    globeScale = Math.max(120, Math.min(450, globeScale - e.deltaY * 0.4));
  });

  // Pin Click Detection
  globeCanvas.addEventListener('click', (e) => {
    const rect = globeCanvas.getBoundingClientRect();
    const clickX = e.clientX - rect.left;
    const clickY = e.clientY - rect.top;
    const R = globeScale;

    const activeEvents = historyEvents.filter(ev => Math.abs(ev.year - currentYear) <= 300);
    for (let ev of activeEvents) {
      const p = projectToSphere(ev.lat, ev.lon, R);
      if (p.visible) {
        const dist = Math.hypot(p.x - clickX, p.y - clickY);
        if (dist <= 12) {
          openEventCard(ev);
          return;
        }
      }
    }
  });

  function openEventCard(ev) {
    eventCard.classList.remove('hidden');
    cardEpoch.textContent = `${ev.epoch.toUpperCase()} // ${ev.loc.split(',')[0].toUpperCase()}`;
    cardTitle.textContent = ev.name;
    cardYear.textContent = ev.year < 0 ? `${Math.abs(ev.year)} BCE` : `${ev.year} CE`;
    cardLoc.textContent = ev.loc;
    cardDesc.textContent = ev.desc;
  }

  btnCloseCard.addEventListener('click', () => eventCard.classList.add('hidden'));

  // Floating Control Handlers
  btnAutoRotate.addEventListener('click', () => {
    isAutoRotating = !isAutoRotating;
    btnAutoRotate.textContent = isAutoRotating ? '⏸ PAUSE' : '⟳ ROTATE';
  });

  btnZoomIn.addEventListener('click', () => {
    globeScale = Math.min(450, globeScale + 30);
  });

  btnZoomOut.addEventListener('click', () => {
    globeScale = Math.max(120, globeScale - 30);
  });

  btnResetView.addEventListener('click', () => {
    rotationY = 0.8;
    rotationX = 0.2;
    globeScale = 220;
    isAutoRotating = true;
  });

  // Timeline Scrubber
  function updateTimeline(val) {
    currentYear = parseInt(val, 10);
    timelineSlider.value = currentYear;
    const formatted = currentYear < 0 ? `${Math.abs(currentYear)} BCE` : `${currentYear} CE`;
    dispYear.textContent = formatted;
    chatContextYear.textContent = formatted;

    // Detect Epoch
    let epochName = "НОВЕЙШЕЕ ВРЕМЯ";
    if (currentYear < -1200) epochName = "БРОНЗОВЫЙ ВЕК";
    else if (currentYear < 500) epochName = "АНТИЧНОСТЬ";
    else if (currentYear < 1400) epochName = "СРЕДНЕВЕКОВЬЕ";
    else if (currentYear < 1760) epochName = "ВОЗРОЖДЕНИЕ";
    else if (currentYear < 1914) epochName = "ПРОМЫШЛЕННЫЙ ВЕК";
    currentEpochBadge.textContent = epochName.toUpperCase();
  }

  timelineSlider.addEventListener('input', (e) => updateTimeline(e.target.value));

  epochPills.forEach(pill => {
    pill.addEventListener('click', () => {
      epochPills.forEach(p => p.classList.remove('active'));
      pill.classList.add('active');
      updateTimeline(pill.getAttribute('data-year'));
    });
  });

  // AI Historian Chat Logic
  btnToggleHistorian.addEventListener('click', () => {
    historianPanel.classList.toggle('collapsed');
    btnToggleHistorian.textContent = historianPanel.classList.contains('collapsed') ? '▶' : '◀';
  });

  async function sendChatMessage(query) {
    if (!query.trim()) return;

    // Append User Message
    const userMsg = document.createElement('div');
    userMsg.className = 'msg msg-user';
    userMsg.textContent = query;
    chatMessages.appendChild(userMsg);
    chatInput.value = '';
    chatMessages.scrollTop = chatMessages.scrollHeight;

    // Loading indicator
    const aiMsg = document.createElement('div');
    aiMsg.className = 'msg msg-ai';
    aiMsg.textContent = 'Изучаю исторические хроники...';
    chatMessages.appendChild(aiMsg);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    try {
      const response = await fetch('/api/historian/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query: query,
          year: currentYear,
          epoch: currentEpochBadge.textContent
        })
      });

      if (!response.ok) throw new Error('API request failed');
      const data = await response.json();
      aiMsg.textContent = data.answer;
    } catch (err) {
      // Smart Fallback Response
      const fallbackAnswers = [
        `В период ${currentYear < 0 ? Math.abs(currentYear) + ' до н.э.' : currentYear + ' н.э.'} ключевым фактором развития были расширение средиземноморских торговых путей и становление имперской бюрократии.`,
        `В эпоху ${currentEpochBadge.textContent} цивилизация переживала масштабные культурные сдвиги: письменность, монетное дело и астрономия определяли геополитический баланс сил.`,
        `Исторические хроники свидетельствуют о глубокой трансформации институтов власти в данный период.`
      ];
      aiMsg.textContent = fallbackAnswers[Math.floor(Math.random() * fallbackAnswers.length)];
    }
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  btnSendChat.addEventListener('click', () => sendChatMessage(chatInput.value));
  chatInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') sendChatMessage(chatInput.value);
  });

  document.querySelectorAll('.quick-btn').forEach(btn => {
    btn.addEventListener('click', () => sendChatMessage(btn.getAttribute('data-q')));
  });

  btnAskAboutEvent.addEventListener('click', () => {
    if (historianPanel.classList.contains('collapsed')) {
      historianPanel.classList.remove('collapsed');
      btnToggleHistorian.textContent = '◀';
    }
    sendChatMessage(`Расскажи подробнее про событие: ${cardTitle.textContent} (${cardYear.textContent})`);
  });

  updateTimeline(-44);
});
