const audioContext = new (window.AudioContext || window.webkitAudioContext)();
const analyser = audioContext.createAnalyser();
const source = audioContext.createMediaElementSource(audioElement);
source.connect(analyser);
analyser.connect(audioContext.destination);

// В вашем рендеринге вы можете использовать данные из анализатора
function render() {
    requestAnimationFrame(render);
    const dataArray = new Uint8Array(analyser.frequencyBinCount);
    analyser.getByteFrequencyData(dataArray);
    
    // Передайте данные в шейдер
    gl.uniform1fv(location, dataArray);
}