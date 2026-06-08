import * as d3 from 'd3';

const width = window.innerWidth;
const height = window.innerHeight - 150; // account for control panel
const svg = d3.select("#graph").append("svg")
    .attr("width", width)
    .attr("height", height);

const colors1 = d3.scaleOrdinal(d3.schemeSet3);
const colors2 = d3.scaleOrdinal(d3.schemePastel1);

let state = {
    step: 0,
    playing: false,
    gear1: null,
    gear2: null,
    total_segments: 0,
    start1_idx: 0,
    start2_idx: 0,
    mode: 'gears',
    cyclesData: {}
};

let g1 = svg.append("g");
let g2 = svg.append("g");
let centerPoint = svg.append("circle").attr("r", 5).attr("fill", "red").style("display", "none");
let intervalId = null;

// UI Elements
const cycle1El = document.getElementById("cycle1");
const cycle2El = document.getElementById("cycle2");
const start1El = document.getElementById("start1");
const start2El = document.getElementById("start2");
const scriptEl = document.getElementById("script");
const modeEl = document.getElementById("mode");
const radius1El = document.getElementById("radius1");
const radius2El = document.getElementById("radius2");
const fontSizeEl = document.getElementById("font-size");

async function init() {
    await fetchCycles();
    
    // Listeners
    cycle1El.addEventListener('change', () => { updateStartDropdowns(); fetchData(); });
    cycle2El.addEventListener('change', () => { updateStartDropdowns(); fetchData(); });
    start1El.addEventListener('change', fetchData);
    start2El.addEventListener('change', fetchData);
    scriptEl.addEventListener('change', () => { fetchCycles().then(fetchData); });
    modeEl.addEventListener('change', () => {
        state.mode = modeEl.value;
        state.step = 0;
        draw();
    });
    radius1El.addEventListener('input', draw);
    radius2El.addEventListener('input', draw);
    fontSizeEl.addEventListener('input', () => {
        svg.selectAll("text").style("font-size", `${fontSizeEl.value}px`);
    });

    fetchData();
}

async function fetchCycles() {
    const scr = scriptEl.value;
    const res = await fetch(`http://localhost:8000/api/cycles?script=${scr}`);
    state.cyclesData = await res.json();
    
    const c1 = cycle1El.value;
    const c2 = cycle2El.value;
    
    cycle1El.innerHTML = '';
    cycle2El.innerHTML = '';
    
    const cycleKeys = Object.keys(state.cyclesData);
    cycleKeys.forEach(key => {
        cycle1El.add(new Option(state.cyclesData[key].name, key));
        cycle2El.add(new Option(state.cyclesData[key].name, key));
    });
    
    cycle1El.value = cycleKeys.includes(c1) ? c1 : (cycleKeys.includes('मास-पक्ष') ? 'मास-पक्ष' : cycleKeys[0]);
    cycle2El.value = cycleKeys.includes(c2) ? c2 : (cycleKeys.includes('वार') ? 'वार' : cycleKeys[1] || cycleKeys[0]);
    
    updateStartDropdowns();
}

function updateStartDropdowns() {
    const c1 = cycle1El.value;
    const c2 = cycle2El.value;
    const s1 = start1El.value;
    const s2 = start2El.value;
    
    start1El.innerHTML = '';
    if (state.cyclesData[c1]) {
        state.cyclesData[c1].items.forEach((item, idx) => start1El.add(new Option(item, idx)));
    }
    
    start2El.innerHTML = '';
    if (state.cyclesData[c2]) {
        state.cyclesData[c2].items.forEach((item, idx) => start2El.add(new Option(item, idx)));
    }
    
    if (s1 && start1El.querySelector(`option[value="${s1}"]`)) start1El.value = s1;
    if (s2 && start2El.querySelector(`option[value="${s2}"]`)) start2El.value = s2;
}

async function fetchData() {
    const c1 = cycle1El.value;
    const c2 = cycle2El.value;
    const s1 = start1El.value;
    const s2 = start2El.value;
    const scr = scriptEl.value;
    const checkValidity = document.getElementById("checkValidity").checked;
    var endpoint;
    // alert("checkValidity:" + restrict);
    const res = await fetch(`http://localhost:8000/api/gears?cycle1=${c1}&cycle2=${c2}&start1=${s1}&start2=${s2}&script=${scr}&checkValidMatching=${checkValidity}`);
    const data = await res.json();
    // console.log("Received data:", data);
        if (data.valid) {
            state.gear1 = data.gear1;
            state.gear2 = data.gear2;
            state.total_segments = data.total_segments;
            state.start1_idx = data.start1_index;
            state.start2_idx = data.start2_index;
            state.alignment = data.alignment;
            state.step = 0; // Reset step on data change
            draw();
        } else {
            alert("The selected pairs are not appropriate, uncheck the restriction to allow for this.");
            return;
        }
    }

function draw() {
    if (!state.gear1 || !state.gear2) return;
    
    g1.selectAll("*").remove();
    g2.selectAll("*").remove();

    const pie1 = d3.pie().value(1).sort(null);
    const pie2 = d3.pie().value(1).sort(null);
    
    let R1_outer, R1_inner, R2_outer, R2_inner;
    let cx1, cx2, cy;

    const R1 = parseInt(radius1El.value) || 150;
    const R2 = parseInt(radius2El.value) || 150;

    if (state.mode === 'gears') {
        cx1 = width / 2 - R1;
        cx2 = width / 2 + R2;
        cy = height / 2;
        
        R1_outer = R1; R1_inner = R1 * 0.4;
        R2_outer = R2; R2_inner = R2 * 0.4;
        
        centerPoint.attr("cx", width / 2).attr("cy", cy).style("display", "block");
    } else {
        // Concentric
        cx1 = cx2 = width / 2;
        cy = height / 2;
        centerPoint.style("display", "none");
        
        R1_outer = R1 * 1.2; R1_inner = R1 * 0.86;
        R2_outer = R2 * 0.86; R2_inner = R2 * 0.4;
    }

    state.cx1 = cx1; state.cx2 = cx2; state.cy = cy;
    const fsize = fontSizeEl.value || 11;

    const arc1 = d3.arc().innerRadius(R1_inner).outerRadius(R1_outer);
    const data1 = Array.from({length: state.gear1.size}).map((_, i) => ({
        value: 1, label: state.gear1.items[(i + state.start1_idx) % state.gear1.size], idx: i
    }));

    const arcs1 = g1.selectAll(".arc1").data(pie1(data1)).enter().append("g").attr("class", "arc1");
    arcs1.append("path").attr("d", arc1).attr("class", "gear-path").attr("fill", d => colors1(d.data.idx));
    arcs1.append("text")
        .attr("transform", d => {
            const centroid = arc1.centroid(d);
            const angle = (d.startAngle + d.endAngle) / 2;
            let rot = (angle * 180 / Math.PI) - 90;
            if (rot > 90 && rot < 270) rot += 180;
            return `translate(${centroid}) rotate(${rot})`;
        })
        .attr("dy", "0.35em")
        .style("text-anchor", "middle")
        .style("font-size", `${fsize}px`)
        .text(d => d.data.label);

    const arc2 = d3.arc().innerRadius(R2_inner).outerRadius(R2_outer);
    const data2 = Array.from({length: state.gear2.size}).map((_, i) => ({
        value: 1, label: state.gear2.items[(i + state.start2_idx) % state.gear2.size], idx: i
    }));
    const arcs2 = g2.selectAll(".arc2").data(pie2(data2)).enter().append("g").attr("class", "arc2");
    arcs2.append("path").attr("d", arc2).attr("class", "gear-path").attr("fill", d => colors2(d.data.idx));
    arcs2.append("text")
        .attr("transform", d => {
            const centroid = arc2.centroid(d);
            const angle = (d.startAngle + d.endAngle) / 2;
            let rot = (angle * 180 / Math.PI) - 90;
            if (rot > 90 && rot < 270) rot += 180;
            return `translate(${centroid}) rotate(${rot})`;
        })
        .attr("dy", "0.35em")
        .style("text-anchor", "middle")
        .style("font-size", `${fsize}px`)
        .text(d => d.data.label);

    applyRotation(0);
}

function applyRotation(duration = 500) {
    if (!state.gear1) return;

    const w1_deg = 360 / state.gear1.size;
    const w2_deg = 360 / state.gear2.size;

    let rot1 = 0, rot2 = 0;

    if (state.mode === 'gears') {
        const base_rot1 = 90 - (w1_deg / 2);
        const base_rot2 = -90 - (w2_deg / 2);
        rot1 = base_rot1 + (state.step * w1_deg);
        rot2 = base_rot2 - (state.step * w2_deg);
    } 
    else if (state.mode === 'sync_concentric') {
        // Both start at top (12 o'clock in D3 is 0deg). 
        // We want the 0th item to be centered at top.
        const base_rot1 = - (w1_deg / 2);
        const base_rot2 = - (w2_deg / 2);
        
        // General alignment based on list length ratios
        const ratioOuterInner = state.gear1.size / state.gear2.size;
        const isIntegerRatioOuterInner = Number.isInteger(ratioOuterInner) && ratioOuterInner > 1;
        const ratioInnerOuter = state.gear2.size / state.gear1.size;
        const isIntegerRatioInnerOuter = Number.isInteger(ratioInnerOuter) && ratioInnerOuter > 1;
        // const innerHasTwoItems = state.gear2.size === 2;
        
        // If outer items span multiple inner items (integer ratio), offset outer by half segment
        // to center the group of outer items with each inner item
        const outerOffset = isIntegerRatioOuterInner ? (-w1_deg / 2) : 0;
        
        // If inner has 2 items, rotate by 90deg for horizontal division
        // const innerOffset = innerHasTwoItems ? 90 : 0;
        const innerOffset = isIntegerRatioInnerOuter ? (-w2_deg / 2) : 0;
        
        rot1 = base_rot1 + outerOffset * (ratioOuterInner-1) - (state.step * w1_deg);
        rot2 = base_rot2 + innerOffset * (ratioInnerOuter-1) - (state.step * w2_deg);
    }
    else if (state.mode === 'concentric') {
        // Static Concentric
        const base_rot1 = - (w1_deg / 2);
        const base_rot2 = - (w2_deg / 2);
        
        // General alignment based on list length ratios
        const ratioOuterInner = state.gear1.size / state.gear2.size;
        const isIntegerRatioOuterInner = Number.isInteger(ratioOuterInner) && ratioOuterInner > 1;
        const ratioInnerOuter = state.gear2.size / state.gear1.size;
        const isIntegerRatioInnerOuter = Number.isInteger(ratioInnerOuter) && ratioInnerOuter > 1;
        // const innerHasTwoItems = state.gear2.size === 2;
        
        // If outer items span multiple inner items (integer ratio), offset outer by half segment
        // to center the group of outer items with each inner item
        const outerOffset = isIntegerRatioOuterInner ? (-w1_deg / 2) : 0;
        
        // If inner has 2 items, rotate by 90deg for horizontal division
        // const innerOffset = innerHasTwoItems ? 90 : 0;
        const innerOffset = isIntegerRatioInnerOuter ? (-w2_deg / 2) : 0;
        
        rot1 = base_rot1 + outerOffset * (ratioOuterInner-1);
        rot2 = base_rot2 + innerOffset * (ratioInnerOuter-1);
    }

    g1.transition().duration(duration).ease(d3.easeCubicInOut)
      .attr("transform", `translate(${state.cx1}, ${state.cy}) rotate(${rot1})`);
      
    g2.transition().duration(duration).ease(d3.easeCubicInOut)
      .attr("transform", `translate(${state.cx2}, ${state.cy}) rotate(${rot2})`);
}

// Playback Controls
document.getElementById('btn-next').addEventListener('click', () => { 
    if(state.mode !== 'concentric') { state.step++; applyRotation(); }
});
document.getElementById('btn-prev').addEventListener('click', () => { 
    if(state.mode !== 'concentric') { state.step--; applyRotation(); }
});
document.getElementById('btn-play').addEventListener('click', () => {
    if(state.mode === 'concentric') return;
    state.playing = !state.playing;
    if (state.playing) {
        intervalId = setInterval(() => { state.step++; applyRotation(); }, 1000);
    } else {
        clearInterval(intervalId);
    }
});

// Handle window resize
window.addEventListener('resize', () => {
    svg.attr("width", window.innerWidth).attr("height", window.innerHeight - 150);
    if(state.gear1) { draw(); }
});

init();
