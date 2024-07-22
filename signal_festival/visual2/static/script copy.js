const fileInput = document.getElementById('fileInput');
const canvas = document.getElementById('visualizer');
const ctx = canvas.getContext('2d');
const audioContext = new (window.AudioContext || window.webkitAudioContext)();
let analyser = audioContext.createAnalyser();
analyser.fftSize = 2048;
const bufferLength = analyser.frequencyBinCount;
const dataArray = new Uint8Array(bufferLength);

canvas.width = window.innerWidth;
canvas.height = window.innerHeight * 0.5; // Увеличиваем высоту для круга

let isPlaying = false;
let audio; // Объявляем переменную для аудио

// Запускаем стандартную визуализацию при загрузке страницы
drawStandardVisualization();

fileInput.addEventListener('change', handleFileSelect);

// Функция для обработки выбора файла
// function handleFileSelect(event) {
//     const file = event.target.files[0];
//     const url = URL.createObjectURL(file);
//     audio = new Audio(url);
//     const source = audioContext.createMediaElementSource(audio);
//     source.connect(analyser);
//     analyser.connect(audioContext.destination);
    
//     // Проверка подключения
//     console.log('Аудио подключено к анализатору');

//     audio.play().then(() => {
//         isPlaying = true;
//         console.log('Аудио воспроизводится');
//         visualize(); // Запускаем визуализацию
//     }).catch(error => {
//         console.error('Ошибка воспроизведения аудио:', error);
//     });

//     // Слушаем событие окончания воспроизведения
//     audio.addEventListener('ended', () => {
//         isPlaying = false; // Возвращаемся к стандартной визуализации
//         drawStandardVisualization();
//     });
// }

function handleFileSelect(event) {
    const file = event.target.files[0];
    const url = URL.createObjectURL(file);
    const audio = new Audio(url);
    const source = audioContext.createMediaElementSource(audio);
    source.connect(analyser);
    analyser.connect(audioContext.destination);
    audio.play();
    visualize();
}


// Функция для визуализации
// function visualize() {
//     requestAnimationFrame(visualize);
    
//     if (isPlaying) {
//         // Визуализация аудио
//         analyser.getByteFrequencyData(dataArray);
        
//         // Проверка, получаем ли данные
//         if (dataArray[0] === 0) {
//             console.log('Нет данных для визуализации');
//         } else {
//             console.log('Данные для визуализации получены:', dataArray);
//         }

//         ctx.fillStyle = 'rgba(0, 0, 0, 0.1)';
//         ctx.fillRect(0, 0, canvas.width, canvas.height);

//         const radius = Math.min(canvas.width, canvas.height) / 2 - 20; // Радиус круга
//         const centerX = canvas.width / 2;
//         const centerY = canvas.height / 2;

//         for (let i = 0; i < bufferLength; i++) {
//             const barHeight = dataArray[i] / 2; // Высота полосы
//             const angle = (i / bufferLength) * Math.PI * 2; // Угол для текущей полосы

//             // Координаты для начала и конца полосы
//             const x1 = centerX + Math.cos(angle) * (radius - barHeight);
//             const y1 = centerY + Math.sin(angle) * (radius - barHeight);
//             const x2 = centerX + Math.cos(angle) * radius;
//             const y2 = centerY + Math.sin(angle) * radius;

//             ctx.beginPath();
//             ctx.moveTo(centerX, centerY);
//             ctx.lineTo(x1, y1);
//             ctx.lineTo(x2, y2);
//             ctx.closePath();
//             ctx.fillStyle = `rgb(0, 0, ${barHeight + 100})`;
//             ctx.fill();
//         }
//     } else {
//         // Стандартная визуализация (бесконечный цикл)
//         drawStandardVisualization();
//     }
// }

// function visualize() {
//     requestAnimationFrame(visualize);
//     analyser.getByteFrequencyData(dataArray);
//     ctx.fillStyle = 'rgba(0, 0, 0, 0.1)';
//     ctx.fillRect(0, 0, canvas.width, canvas.height);
//     const barWidth = (canvas.width / bufferLength) * 2.5;
//     let barHeight;
//     let x = 0;

//     for (let i = 0; i < bufferLength; i++) {
//         barHeight = dataArray[i] / 2;
//         ctx.fillStyle = `rgb(0, 0, ${barHeight + 100})`;
//         ctx.fillRect(x, canvas.height - barHeight / 2, barWidth, barHeight);
//         x += barWidth + 1;
//     }
// }
//работает почти круг
// function visualize2() {
//     requestAnimationFrame(visualize);
//     analyser.getByteFrequencyData(dataArray);
//     ctx.fillStyle = 'rgba(0, 0, 0, 0.1)';
//     ctx.fillRect(0, 0, canvas.width, canvas.height);
    
//     const radius = 100; // Радиус окружности
//     const centerX = canvas.width / 2; // Центр по оси X
//     const centerY = canvas.height / 2; // Центр по оси Y
//     const barCount = bufferLength; // Количество "баров" (или кругов)
//     const angleStep = (2 * Math.PI) / barCount; // Угол между кругами

//     for (let i = 0; i < barCount; i++) {
//         const barHeight = dataArray[i] / 2; // Высота круга
//         const angle = i * angleStep; // Угол для текущего круга

//         // Вычисляем координаты для круга
//         const x = centerX + radius * Math.cos(angle);
//         const y = centerY + radius * Math.sin(angle);

//         // Устанавливаем цвет круга
//         ctx.fillStyle = `rgb(0, 0, ${barHeight + 100})`;

//         // Рисуем круг
//         ctx.beginPath();
//         ctx.arc(x, y, barHeight, 0, Math.PI * 2);
//         ctx.fill();
//     }
// }
// function visualize() {
//     requestAnimationFrame(visualize);
//     analyser.getByteFrequencyData(dataArray);
//     ctx.fillStyle = 'rgba(0, 0, 0, 0.1)';
//     ctx.fillRect(0, 0, canvas.width, canvas.height);
    
//     const radius = 200; // Радиус окружности
//     const centerX = canvas.width / 2; // Центр по оси X
//     const centerY = canvas.height / 2; // Центр по оси Y
//     const barCount = bufferLength; // Количество "баров" (или кругов)
//     const angleStep = (2 * Math.PI) / barCount; // Угол между кругами

//     for (let i = 0; i < barCount; i++) {
//         const barHeight = dataArray[i] / 2; // Высота круга
//         const angle = i * angleStep; // Угол для текущего круга

//         // Вычисляем координаты для круга
//         const x = centerX + radius * Math.cos(angle);
//         const y = centerY + radius * Math.sin(angle);

//         // Устанавливаем цвет круга с эффектом пульсации
//         const colorValue = Math.min(255, barHeight + 100);
//         ctx.fillStyle = `rgb(0, ${colorValue}, ${colorValue})`;

//         // Рисуем круг с эффектом пульсацииы
//         ctx.beginPath();
//         ctx.arc(x, y, barHeight, 0, Math.PI * 2);
//         ctx.fill();

//         // Добавляем эффект "пульсации" с помощью изменения радиуса
//         const pulseRadius = barHeight * 0.5; // Пульсация
//         ctx.beginPath();
//         ctx.arc(x, y, pulseRadius, 0, Math.PI * 2);
//         ctx.fillStyle = `rgba(255, 255, 255, 0.2)`; // Полупрозрачный белый
//         ctx.fill();
//     }
// }
const particles = [];
const lines = [];
const shapes = [];
const maxParticles = 100; // Максимальное количество частиц
const maxLines = 50; // Максимальное количество линий
const maxShapes = 20; // Максимальное количество фигур

// Функция для создания случайной частицы
function createParticle() {
    return {
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        radius: Math.random() * 5 + 2, // Случайный радиус
        color: `rgba(${Math.random() * 255}, ${Math.random() * 255}, ${Math.random() * 255}, 0.7)`,
        speedX: (Math.random() - 0.5) * 2, // Случайная скорость по X
        speedY: (Math.random() - 0.5) * 2  // Случайная скорость по Y
    };
}

// Функция для создания случайной линии
function createLine() {
    return {
        x1: Math.random() * canvas.width,
        y1: Math.random() * canvas.height,
        x2: Math.random() * canvas.width,
        y2: Math.random() * canvas.height,
        color: `rgba(${Math.random() * 255}, ${Math.random() * 255}, ${Math.random() * 255}, 0.5)`,
        width: Math.random() * 2 + 1 // Случайная ширина линии
    };
}

// Функция для создания случайной фигуры
function createShape() {
    return {
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        size: Math.random() * 20 + 10, // Случайный размер
        color: `rgba(${Math.random() * 255}, ${Math.random() * 255}, ${Math.random() * 255}, 0.5)`,
        type: Math.random() < 0.5 ? 'circle' : 'square' // Случайный тип фигуры
    };
}

// Инициализация частиц, линий и фигур
for (let i = 0; i < maxParticles; i++) {
    particles.push(createParticle());
}
for (let i = 0; i < maxLines; i++) {
    lines.push(createLine());
}
for (let i = 0; i < maxShapes; i++) {
    shapes.push(createShape());
}

function visualize() {
    requestAnimationFrame(visualize);
    analyser.getByteFrequencyData(dataArray);
    ctx.fillStyle = 'rgba(0, 0, 0, 0.1)';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    const radius = 100; // Радиус окружности
    const centerX = canvas.width / 2; // Центр по оси X
    const centerY = canvas.height / 2; // Центр по оси Y
    const barCount = bufferLength; // Количество "баров" (или кругов)
    const angleStep = (2 * Math.PI) / barCount; // Угол между кругами

    // Рисуем круги эквалайзера
    for (let i = 0; i < barCount; i++) {
        const barHeight = dataArray[i] / 2; // Высота круга
        const angle = i * angleStep; // Угол для текущего круга

        // Вычисляем координаты для круга
        const x = centerX + radius * Math.cos(angle);
        const y = centerY + radius * Math.sin(angle);

        // Устанавливаем цвет круга с эффектом пульсации
        const colorValue = Math.min(255, barHeight + 100);
        ctx.fillStyle = `rgb(0, ${colorValue}, ${colorValue})`;

        // Рисуем круг
        ctx.beginPath();
        ctx.arc(x, y, barHeight, 0, Math.PI * 2);
        ctx.fill();

        // Добавляем эффект "пульсации"
        const pulseRadius = barHeight * 0.5; // Пульсация
        ctx.beginPath();
        ctx.arc(x, y, pulseRadius, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(255, 255, 255, 0.2)`; // Полупрозрачный белый
        ctx.fill();
    }

    // Рисуем частицы
    particles.forEach(particle => {
        ctx.beginPath();
        ctx.arc(particle.x, particle.y, particle.radius, 0, Math.PI * 2);
        ctx.fillStyle = particle.color;
        ctx.fill();

        // Обновляем позицию частицы
        particle.x += particle.speedX;
        particle.y += particle.speedY;

        // Проверка на границы
        if (particle.x < 0 || particle.x > canvas.width) particle.speedX *= -1;
        if (particle.y < 0 || particle.y > canvas.height) particle.speedY *= -1;
    });

    // Рисуем линии
    lines.forEach(line => {
        ctx.beginPath();
        ctx.moveTo(line.x1, line.y1);
        ctx.lineTo(line.x2, line.y2);
        ctx.lineWidth = line.width;
        ctx.strokeStyle = line.color;
        ctx.stroke();
    });

    // Рисуем фигуры
    shapes.forEach(shape => {
        ctx.fillStyle = shape.color;
        if (shape.type === 'circle') {
            ctx.beginPath();
            ctx.arc(shape.x, shape.y, shape.size, 0, Math.PI * 2);
            ctx.fill();
        } else {
            ctx.fillRect(shape.x, shape.y, shape.size, shape.size);
        }
    });
}

// Функция для стандартной визуализации
function drawStandardVisualization() {
    ctx.fillStyle = 'rgba(0, 0, 0, 0.1)';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    const barCount = 30; // Количество полос
    const barWidth = canvas.width / barCount;
    
    for (let i = 0; i < barCount; i++) {
        const height = Math.random() * (canvas.height / 2);
        ctx.fillStyle = `rgb(0, 0, ${height + 100})`;
        ctx.fillRect(i * barWidth, canvas.height - height, barWidth - 2, height);
    }
}