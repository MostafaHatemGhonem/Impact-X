// Flask API Helper - يعمل مع Flask و Pywebview
const isFlaskMode = !(window as any).pywebview;

const API = {
  async run_simulation(
    asteroid_name: string,
    diameter: string | null,
    velocity: string,
    latitude: string,
    longitude: string,
    h?: string
  ): Promise<any> {
    if (isFlaskMode) {
      // Flask mode
      const response = await fetch('/api/run_simulation', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          asteroid_name: asteroid_name,
          diameter: diameter,
          velocity: velocity,
          lat: latitude,
          long: longitude,
          h_value: h,
          v_inf_value: velocity
        })
      });
      return await response.text();
    } else {
      // Pywebview mode
      return await (window as any).pywebview.api.run_simulation(
        asteroid_name, diameter, velocity, latitude, longitude, h
      );
    }
  },

  async get_asteroid_list(): Promise<string> {
    if (isFlaskMode) {
      // Flask mode
      const response = await fetch('/api/get_asteroid_list');
      return await response.text();
    } else {
      // Pywebview mode - الصح هنا
      return await (window as any).pywebview.api.get_asteroid_list();
    }
  }
};

function TypingEffect(words: string[], target: HTMLElement, container: HTMLElement) {
  const typingSpeed: number = 60;
  let isRunning = false;

  async function startTyping() {
    if (isRunning) return;
    isRunning = true;

    for (let i = 0; i < words.length; i++) {
      await typeLine(words[i]!);
      if (i < words.length - 1) {
        target.innerHTML += '<br>';
        await wait(350);
      }
    }
  }

  function wait(ms: number) {
    return new Promise(res => setTimeout(res, ms));
  }

  async function typeLine(line: string) {
    for (let ch of line) {
      target.innerHTML += ch;
      await wait(typingSpeed + Math.floor(Math.random() * 20 - 10));
    }
  }

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        startTyping();
      }
    });
  }, { threshold: 0.6 });

  observer.observe(container);
}

function safeNum(n: any, decimals: number = 2) {
  const num = Number(n);
  if (!Number.isFinite(num)) return 'N/A';
  return num.toFixed(decimals);
}

let mainPage: HTMLElement;
let pageFour: HTMLElement;
let isPageFourActive: boolean = false;

const saveScenarios = [
  {
    id: 1,
    name: "Deflection Mission Success",
    description: "NASA's DART mission successfully deflected the asteroid",
    diameter: "0.001",
    velocity: "5",
    message: "Mission accomplished! The asteroid was deflected with minimal impact."
  },
  {
    id: 2,
    name: "Nuclear Disruption",
    description: "Nuclear device fragmented the asteroid into smaller pieces",
    diameter: "0.05",
    velocity: "8",
    message: "The asteroid was broken into smaller fragments. Minor impacts expected."
  },
  {
    id: 3,
    name: "Gravity Tractor",
    description: "Slow deflection over years using spacecraft gravity",
    diameter: "0.01",
    velocity: "6",
    message: "Successful long-term deflection. The asteroid passed safely by Earth."
  },
  {
    id: 4,
    name: "Last-Minute Evacuation",
    description: "Unable to stop the asteroid, but evacuated the impact zone",
    diameter: "0.1",
    velocity: "12",
    message: "Impact occurred but all residents were safely evacuated beforehand."
  },
  {
    id: 5,
    name: "Kinetic Impactor",
    description: "High-speed spacecraft collision changed asteroid trajectory",
    diameter: "0.02",
    velocity: "7",
    message: "Kinetic impact successful. Asteroid trajectory altered significantly."
  }
];

function createVideoElement(src: string, className: string): HTMLVideoElement {
  const video = document.createElement("video");
  video.classList.add(className);
  
  const source = document.createElement("source");
  source.src = src;
  source.type = "video/mp4";
  video.appendChild(source);
  
  video.setAttribute("playsinline", "");
  video.setAttribute("webkit-playsinline", "");
  video.muted = true;
  video.loop = true;
  video.preload = "auto";
  video.autoplay = true;
  
  video.addEventListener('loadeddata', () => {
    video.play().catch(err => {
      console.log("Autoplay prevented:", err);
      document.addEventListener('click', () => video.play(), { once: true });
    });
  });
  
  setTimeout(() => {
    if (video.paused) video.play().catch(e => console.log("Delayed play failed:", e));
  }, 500);
  
  video.load();
  return video;
}

async function callPythonSimulation(
  asteroid_name: string,
  diameter: string | null,
  velocity: string,
  latitude: string,
  longitude: string,
  h?: string
) {
  const containerFiveInputs = document.querySelector(".containerFiveInputs") as HTMLElement;
  if (containerFiveInputs) {
    const containerFiveInputs = document.querySelector(".containerFiveInputs") as HTMLElement;
    containerFiveInputs.innerHTML = "";
    
    let loadingPage = document.createElement("div");
    loadingPage.classList.add("loadingPage");
    let loadingVideo = createVideoElement("./assit/videos/3657852753-preview.mp4", "loadingVideo");
    loadingPage.appendChild(loadingVideo);
    let loadingText = document.createElement("p");
    loadingText.classList.add("loadingText");
    loadingPage.appendChild(loadingText);
    containerFiveInputs.appendChild(loadingPage);
    
    TypingEffect(["Loading asteroids..."], loadingText, loadingPage);
  }
  
  try {
    console.log("Calling simulation...");
    const response = await API.run_simulation(
      asteroid_name, diameter, velocity, latitude, longitude, h
    );

    let resultData: any;
    try {
      resultData = typeof response === 'string' ? JSON.parse(response) : response;
    } catch (err) {
      resultData = { error: 'Invalid response from simulation' };
    }

    console.log("Simulation complete:", resultData);

    if (resultData && resultData.error) {
      const msg = String(resultData.error);
      if (containerFiveInputs) {
        containerFiveInputs.innerHTML = `<p class="text-danger">Error: ${msg}</p>`;
      }
      return;
    }

    displaySimulationResults(resultData);
  } catch (error) {
    console.error("Error running simulation:", error);
    if (containerFiveInputs) {
      containerFiveInputs.innerHTML = `<p class="text-danger">Error: ${error}</p>`;
    }
  }
}

function displaySimulationResults(resultData: any) {
  const containerFiveInputs = document.querySelector(".containerFiveInputs") as HTMLElement;
  if (!containerFiveInputs) return;

  containerFiveInputs.innerHTML = "";

  let resultDiv = document.createElement("div");
  resultDiv.classList.add("results", "mt-4");

  let resultGroup = document.createElement("div");
  resultGroup.classList.add("result-group");
  resultDiv.appendChild(resultGroup);

  let h2 = document.createElement("h2");
  h2.classList.add("text-center");
  h2.textContent = "Simulation Results";
  resultGroup.appendChild(h2);

  let p = document.createElement("p");
  p.classList.add("mb-2");
  p.textContent = "Mass: " + safeNum(resultData.mass_kg, 2) + " kg";
  resultGroup.appendChild(p);

  let p2 = document.createElement("p");
  p2.classList.add("mb-2");
  p2.textContent = "Kinetic energy: " + safeNum(resultData.energy_joules, 2) + " Joules";
  resultGroup.appendChild(p2);

  let p3 = document.createElement("p");
  p3.classList.add("mb-2");
  p3.textContent = "Megatons TNT: " + safeNum(resultData.megatons_tnt, 2);
  resultGroup.appendChild(p3);

  let p4 = document.createElement("p");
  p4.classList.add("mb-2");
  p4.textContent = "Crater Diameter: " + safeNum(resultData.crater_diameter_km, 2) + " km";
  resultGroup.appendChild(p4);

  if (resultData.is_ocean_impact) {
    let p5 = document.createElement("p");
    p5.classList.add("mb-2");
    p5.textContent = "Tsunami height: " + safeNum(resultData.tsunami_height_m, 2) + " m";
    resultGroup.appendChild(p5);
  } else {
    let p6 = document.createElement("p");
    p6.classList.add("mb-2");
    p6.textContent = "Crater Depth: " + safeNum(resultData.crater_depth_km, 2) + " km";
    resultGroup.appendChild(p6);
  
    let p7 = document.createElement("p");
    p7.classList.add("mb-2");
    p7.textContent = "Earthquake Magnitude: " + 
      safeNum(resultData.earthquake_magnitude, 2) + " Richter";
    resultGroup.appendChild(p7);
  }

  let p8 = document.createElement("h3");
  p8.classList.add("mb-2");
  p8.textContent = "Impact location";
  resultGroup.appendChild(p8);

  if (resultData.map_html) {
    const iframe = document.createElement('iframe');
    iframe.classList.add('map-container');
    iframe.style.width = '100%';
    iframe.style.height = '400px';
    iframe.style.borderRadius = '8px';
    iframe.style.border = 'none';
    iframe.srcdoc = resultData.map_html;
    iframe.sandbox.add('allow-scripts');
    resultGroup.appendChild(iframe);
  } else {
    let p9 = document.createElement("p");
    p9.textContent = "Map not available.";
    resultGroup.appendChild(p9);
  }

  containerFiveInputs.appendChild(resultDiv);
}

function pageFourDystriod() {
  ['pageFour', 'pageFive', 'pageSix'].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.remove();
  });
  
  isPageFourActive = true;
  pageFour = document.createElement("div");
  pageFour.id = "pageFour";
  pageFour.classList.add("pageFour", "container", "pageFourDystriod");

  let titlePageDystriod = document.createElement("h1");
  titlePageDystriod.classList.add("titlePageDystriod");
  pageFour.appendChild(titlePageDystriod);
  TypingEffect(["Destroy Earth"], titlePageDystriod, pageFour);
  
  let containerDystriod = document.createElement("div");
  containerDystriod.classList.add("containerDystriod");

  let addYourAstreriod = document.createElement("button");
  addYourAstreriod.classList.add("addYourAstreriod");
  addYourAstreriod.textContent = "Add Your Asteroid";
  
  addYourAstreriod.addEventListener("click", () => {
    const existingPageFive = document.getElementById("pageFive");
    if (existingPageFive) existingPageFive.remove();
    
    let pageFive = document.createElement("div");
    pageFive.id = "pageFive";
    pageFive.classList.add("pageFive", "container");
    
    let containerFive = document.createElement("div");
    containerFive.classList.add("containerFive");
    
    let containerFiveInputs = document.createElement("div");
    containerFiveInputs.classList.add("containerFiveInputs");
    containerFive.appendChild(containerFiveInputs);
    
    let containerDiamter = document.createElement("div");
    containerDiamter.classList.add("containerDiamter");
    let diameter = document.createElement("input");
    diameter.type = "number";
    diameter.placeholder = "Diameter (km)";
    diameter.classList.add("diameter");
    containerDiamter.appendChild(diameter);
    containerFiveInputs.appendChild(containerDiamter);
    
    let containerVelocity = document.createElement("div");
    containerVelocity.classList.add("containerVelocity");
    let velocity = document.createElement("input");
    velocity.type = "number";
    velocity.placeholder = "Velocity (km/s)";
    velocity.classList.add("velocity");
    containerVelocity.appendChild(velocity);
    containerFiveInputs.appendChild(containerVelocity);
    
    let containerLatitude = document.createElement("div");
    containerLatitude.classList.add("containerLatitude");
    let latitude = document.createElement("input");
    latitude.type = "number";
    latitude.max = "90";
    latitude.min = "-90";
    latitude.classList.add("latitude");
    latitude.placeholder = "Latitude";
    containerLatitude.appendChild(latitude);
    containerFiveInputs.appendChild(containerLatitude);
    
    let containerLongitude = document.createElement("div");
    containerLongitude.classList.add("containerLongitude");
    let longitude = document.createElement("input");
    longitude.type = "number";
    longitude.max = "180";
    longitude.min = "-180";
    longitude.classList.add("longitude");
    longitude.placeholder = "Longitude";
    containerLongitude.appendChild(longitude);
    containerFiveInputs.appendChild(containerLongitude);
    
    let generate = document.createElement("button");
    generate.textContent = "Generate";
    generate.classList.add("generate");
    containerFiveInputs.appendChild(generate);
    
    let containerAnmations = document.createElement("div");
    containerAnmations.classList.add("containerAnmations");
    let Earth = createVideoElement("./assit/videos/Earth destroyed.mp4", "Earth");
    containerAnmations.appendChild(Earth);
    containerFive.appendChild(containerAnmations);

    pageFive.appendChild(containerFive);
    mainPage.appendChild(pageFive);
    pageFive.scrollIntoView({ behavior: "smooth" });
    
    generate.addEventListener("click", () => {
      if (!diameter.value || !velocity.value || !latitude.value || !longitude.value) {
        alert("Please fill all fields");
        return;
      }
      callPythonSimulation("", diameter.value, velocity.value, latitude.value, longitude.value);
    });
  });

  let choseYourAstreriod = document.createElement("button");
  choseYourAstreriod.classList.add("choseYourAstreriod");
  choseYourAstreriod.textContent = "Choose Your Asteroid";

  choseYourAstreriod.addEventListener("click", async function() {
    if (!document.getElementById("pageFive")) {
      let pageFive = document.createElement("div");
      pageFive.id = "pageFive";
      pageFive.classList.add("pageFive", "container");
      
      let containerFive = document.createElement("div");
      containerFive.classList.add("containerFive");
      
      let containerFiveInputs = document.createElement("div");
      containerFiveInputs.classList.add("containerFiveInputs");
      containerFive.appendChild(containerFiveInputs);

      let containerAnmations = document.createElement("div");
      containerAnmations.classList.add("containerAnmations");
      let Earth = createVideoElement("./assit/videos/Earth destroyed.mp4", "Earth");
      containerAnmations.appendChild(Earth);
      containerFive.appendChild(containerAnmations);

      pageFive.appendChild(containerFive);
      mainPage.appendChild(pageFive);
    }

    const containerFiveInputs = document.querySelector(".containerFiveInputs") as HTMLElement;
    containerFiveInputs.innerHTML = "";
    
    let loadingPage = document.createElement("div");
    loadingPage.classList.add("loadingPage");
    let loadingVideo = createVideoElement("./assit/videos/3657852753-preview.mp4", "loadingVideo");
    loadingPage.appendChild(loadingVideo);
    let loadingText = document.createElement("p");
    loadingText.classList.add("loadingText");
    loadingPage.appendChild(loadingText);
    containerFiveInputs.appendChild(loadingPage);
    
    TypingEffect(["Loading asteroids..."], loadingText, loadingPage);

    const pageFive = document.getElementById("pageFive");
    if (pageFive) pageFive.scrollIntoView({ behavior: "smooth" });

    try {
      const jsonString = await API.get_asteroid_list();
      const asteroidList = JSON.parse(jsonString);
      containerFiveInputs.innerHTML = "";

      if(asteroidList.error){
        containerFiveInputs.innerHTML = `<p class="text-danger">Error: ${asteroidList.error}</p>`;
        return;
      }
      
      if(asteroidList.length > 0){
        let select = document.createElement("select");
        select.classList.add("asteroidSelect");
        let defaultOption = document.createElement("option");
        defaultOption.value = "";
        defaultOption.textContent = "Select an Asteroid";
        select.appendChild(defaultOption);

        asteroidList.forEach((asteroid: any) => {
          let option = document.createElement("option");
          option.value = asteroid.name;
          option.textContent = asteroid.name;
          option.dataset.h = asteroid.h;
          option.dataset.v_inf = asteroid.v_inf;
          select.appendChild(option);
        });
        containerFiveInputs.appendChild(select);

        let latitude = document.createElement("input");
        latitude.type = "number";
        latitude.max = "90";
        latitude.min = "-90";
        latitude.classList.add("latitude");
        latitude.placeholder = "Latitude";
        containerFiveInputs.appendChild(latitude);

        let longitude = document.createElement("input");
        longitude.type = "number";
        longitude.max = "180";
        longitude.min = "-180";
        longitude.classList.add("longitude");
        longitude.placeholder = "Longitude";
        containerFiveInputs.appendChild(longitude);

        let launchButton = document.createElement("button");
        launchButton.textContent = "Launch Simulation";
        launchButton.classList.add("launchButton");
        containerFiveInputs.appendChild(launchButton);

        launchButton.addEventListener("click", () => {
          const selectedOption = select.options[select.selectedIndex];
          if (!selectedOption || !selectedOption.value) {
            alert("Please select an asteroid");
            return;
          }
          
          if (!latitude.value || !longitude.value) {
            alert("Please enter coordinates");
            return;
          }

          const h = selectedOption.dataset.h;
          const v_inf = selectedOption.dataset.v_inf;

          if (!h || !v_inf) {
            alert("Invalid asteroid data");
            return;
          }

          callPythonSimulation(selectedOption.value, null, v_inf, latitude.value, longitude.value, h);
        });
      } else {
        containerFiveInputs.innerHTML = `<p class="text-danger">No asteroids available</p>`;
      }
    } catch (error) {
      console.error("Error fetching asteroids:", error);
      containerFiveInputs.innerHTML = `<p class="text-danger">Error: ${error}</p>`;
    }
  });
  
  containerDystriod.appendChild(addYourAstreriod);
  containerDystriod.appendChild(choseYourAstreriod);
  pageFour.appendChild(containerDystriod);
  mainPage.appendChild(pageFour);
  pageFour.scrollIntoView({ behavior: "smooth" });
}

function pageFourSave() {
  ['pageFour', 'pageFive', 'pageSix'].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.remove();
  });
  
  isPageFourActive = true;
  pageFour = document.createElement("div");
  pageFour.id = "pageFour";
  pageFour.classList.add("pageFour", "container", "pageFourSave");
  
  let titlePageSave = document.createElement("h1");
  titlePageSave.classList.add("titlePageSave");
  pageFour.appendChild(titlePageSave);
  TypingEffect(["Save The World"], titlePageSave, pageFour);
  
  let descriptionDiv = document.createElement("div");
  descriptionDiv.classList.add("saveDescription");
  let descText = document.createElement("p");
  descriptionDiv.appendChild(descText);
  pageFour.appendChild(descriptionDiv);
  
  setTimeout(() => {
    TypingEffect(["Choose a scenario where humanity successfully prevented catastrophic impact:"], descText, descriptionDiv);
  }, 1500);
  
  let scenariosContainer = document.createElement("div");
  scenariosContainer.classList.add("scenariosContainer");
  
  saveScenarios.forEach(scenario => {
    let card = document.createElement("div");
    card.classList.add("scenarioCard");
    
    let cardTitle = document.createElement("h3");
    cardTitle.textContent = scenario.name;
    card.appendChild(cardTitle);
    
    let cardDesc = document.createElement("p");
    cardDesc.classList.add("scenarioDesc");
    cardDesc.textContent = scenario.description;
    card.appendChild(cardDesc);
    
    let selectBtn = document.createElement("button");
    selectBtn.classList.add("selectScenarioBtn");
    selectBtn.textContent = "Select This Scenario";
    selectBtn.addEventListener("click", () => showScenarioSimulation(scenario));
    card.appendChild(selectBtn);
    
    scenariosContainer.appendChild(card);
  });
  
  pageFour.appendChild(scenariosContainer);
  mainPage.appendChild(pageFour);
  pageFour.scrollIntoView({ behavior: "smooth" });
}

function showScenarioSimulation(scenario: any) {
  let pageSix = document.getElementById("pageSix") as HTMLElement;
  if (!pageSix) {
    pageSix = document.createElement("div");
    pageSix.id = "pageSix";
    pageSix.classList.add("pageSix", "container");
    mainPage.appendChild(pageSix);
  }
  
  pageSix.innerHTML = "";
  
  let scenarioTitle = document.createElement("h2");
  scenarioTitle.classList.add("scenarioTitle");
  pageSix.appendChild(scenarioTitle);
  TypingEffect([scenario.name], scenarioTitle, pageSix);
  
  let scenarioMessage = document.createElement("div");
  scenarioMessage.classList.add("scenarioMessage");
  let messageText = document.createElement("p");
  messageText.classList.add("messageText");
  scenarioMessage.appendChild(messageText);
  pageSix.appendChild(scenarioMessage);
  
  setTimeout(() => {
    TypingEffect([scenario.message], messageText, scenarioMessage);
  }, 2000);
  
  let locationContainer = document.createElement("div");
  locationContainer.classList.add("locationContainer");
  let locationTitle = document.createElement("h3");
  locationContainer.appendChild(locationTitle);
  pageSix.appendChild(locationContainer);
  
  setTimeout(() => {
    TypingEffect(["Verify Impact Zone (Former Threat Location)"], locationTitle, locationContainer);
  }, 3500);
  
  let latInput = document.createElement("input");
  latInput.type = "number";
  latInput.placeholder = "Latitude";
  latInput.classList.add("latitude");
  latInput.max = "90";
  latInput.min = "-90";
  latInput.value = "0";
  locationContainer.appendChild(latInput);
  
  let lonInput = document.createElement("input");
  lonInput.type = "number";
  lonInput.placeholder = "Longitude";
  lonInput.classList.add("longitude");
  lonInput.max = "180";
  lonInput.min = "-180";
  lonInput.value = "0";
  locationContainer.appendChild(lonInput);
  
  let simulateBtn = document.createElement("button");
  simulateBtn.classList.add("generate");
  simulateBtn.textContent = "View Saved Area on Map";
  locationContainer.appendChild(simulateBtn);
  
  let resultsDiv = document.createElement("div");
  resultsDiv.classList.add("scenarioResults");
  pageSix.appendChild(resultsDiv);
  
  simulateBtn.addEventListener("click", async () => {
    resultsDiv.innerHTML = "<p class='text-info text-center'>Generating map...</p>";
    
    try {
      const response = await API.run_simulation(
        `Save_${scenario.id}`,
        scenario.diameter,
        scenario.velocity,
        latInput.value,
        lonInput.value
      );
      
      const resultData = JSON.parse(response);
      displaySaveScenarioResults(resultData, scenario, resultsDiv);
    } catch (error) {
      console.error("Error:", error);
      resultsDiv.innerHTML = `<p class="text-danger">Error generating simulation.</p>`;
    }
  });
  
  pageSix.scrollIntoView({ behavior: "smooth" });
}

function displaySaveScenarioResults(resultData: any, scenario: any, container: HTMLElement) {
  container.innerHTML = "";
  
  let successCard = document.createElement("div");
  successCard.classList.add("successCard");
  
  let successTitle = document.createElement("h2");
  successTitle.classList.add("text-center", "successTitle");
  successCard.appendChild(successTitle);
  TypingEffect(["✓ Threat Neutralized"], successTitle, successCard);
  
  let impactData = document.createElement("div");
  impactData.classList.add("impactData");
  
  let p1 = document.createElement("p");
  p1.classList.add("mb-2");
  p1.innerHTML = `<strong>Original Threat:</strong> Asteroid ${(parseFloat(scenario.diameter) * 1000).toFixed(1)}m at ${scenario.velocity} km/s`;
  impactData.appendChild(p1);
  
  let p2 = document.createElement("p");
  p2.classList.add("mb-2");
  p2.innerHTML = `<strong>Actual Impact Energy:</strong> ${safeNum(resultData.megatons_tnt, 6)} Megatons TNT (Minimal)`;
  impactData.appendChild(p2);
  
  let p3 = document.createElement("p");
  p3.classList.add("mb-2");
  p3.innerHTML = `<strong>Crater Diameter:</strong> ${safeNum(resultData.crater_diameter_km, 3)} km (Negligible)`;
  impactData.appendChild(p3);
  
  let p4 = document.createElement("p");
  p4.classList.add("mb-2", "success-text");
  p4.innerHTML = `<strong>Status:</strong> ${scenario.message}`;
  impactData.appendChild(p4);
  
  let p5 = document.createElement("p");
  p5.classList.add("mb-2", "success-text");
  p5.innerHTML = `<strong>Casualties:</strong> Zero - Mission Success!`;
  impactData.appendChild(p5);
  
  successCard.appendChild(impactData);
  
  if (resultData.map_html) {
    let mapTitle = document.createElement("h3");
    mapTitle.classList.add("mb-2");
    mapTitle.textContent = "Saved Location";
    successCard.appendChild(mapTitle);

    const iframe = document.createElement('iframe');
    iframe.classList.add('map-container');
    iframe.style.width = '100%';
    iframe.style.height = '400px';
    iframe.style.borderRadius = '8px';
    iframe.style.border = 'none';
    iframe.srcdoc = resultData.map_html;
    iframe.sandbox.add('allow-scripts');
    successCard.appendChild(iframe);
  }
  
  container.appendChild(successCard);
}

document.addEventListener('DOMContentLoaded', () => {
  console.log(`DOM Loaded - Mode: ${isFlaskMode ? 'Flask' : 'Pywebview'}`);
  
  mainPage = document.querySelector(".mainPage") as HTMLElement;
  if (!mainPage) {
    console.error("mainPage not found!");
    return;
  }
  
  // Force play HTML videos
  document.querySelectorAll('video').forEach(video => {
    video.muted = true;
    video.play().catch(() => {
      document.addEventListener('click', () => video.play(), { once: true });
    });
  });
  
  setTimeout(() => {
    const pageOne = document.getElementById("pageOne");
    if (pageOne) {
      const mainTitle = pageOne.querySelector(".maintitle") as HTMLElement;
      if (mainTitle) {
        TypingEffect(["when the sky strikes back"], mainTitle, pageOne);
      }
    }
  }, 300);
  
  const pageTwo = document.getElementById("pageTwo");
  if (pageTwo) {
    const titlePageMain = pageTwo.querySelector(".mainTitlePage") as HTMLElement;
    if (titlePageMain) {
      TypingEffect(["Meteor Madness"], titlePageMain, pageTwo);
    }
    
    const titlePage2 = pageTwo.querySelector(".titlePage2") as HTMLElement;
    if (titlePage2) {
      TypingEffect([
        "Welcome to Meteor Madness Infinity Explorers EG",
        "We explore the universe together!"
      ], titlePage2, pageTwo);
    }
  }
  
  const dystriodVideo = document.querySelector(".dystriodVideo") as HTMLElement;
  const dystriodEarthBtn = document.querySelector(".dystriodEarthBtn") as HTMLButtonElement;
  const saveVideo = document.querySelector(".saveVideo") as HTMLElement;
  const saveEarthBtn = document.querySelector(".saveEarthBtn") as HTMLButtonElement;
  
  if (dystriodVideo) {
    dystriodVideo.addEventListener("click", pageFourDystriod);
  }
  
  if (dystriodEarthBtn) {
    dystriodEarthBtn.addEventListener("click", pageFourDystriod);
  }
  
  if (saveVideo) {
    saveVideo.addEventListener("click", pageFourSave);
  }
  
  if (saveEarthBtn) {
    saveEarthBtn.addEventListener("click", pageFourSave);
  }
  
  console.log("All event listeners attached");
});