const carModels = {
    "Acura": ["ILX", "MDX", "RDX", "RLX", "TLX", "NSX"],
    "Alfa Romeo": ["Giulia", "Stelvio", "Tonale", "4C", "Giulietta"],
    "Aston Martin": ["DB11", "DB12", "Vantage", "DBS", "DBX"],
    "Audi": ["A1", "A3", "A4", "A5", "A6", "A7", "A8", "Q2", "Q3", "Q5", "Q7", "Q8", "TT", "R8", "e-tron"],
    "Bentley": ["Bentayga", "Continental GT", "Flying Spur", "Mulsanne"],
    "BMW": ["1 Series", "2 Series", "3 Series", "4 Series", "5 Series", "6 Series", "7 Series", "8 Series", "X1", "X2", "X3", "X4", "X5", "X6", "X7", "Z4", "M2", "M3", "M4", "M5", "i3", "i4", "i7", "iX"],
    "Bugatti": ["Chiron", "Veyron", "Divo", "Bolide"],
    "Buick": ["Enclave", "Encore", "Envision", "LaCrosse"],
    "BYD": ["Atto 3", "Han", "Tang", "Seal", "Dolphin", "Song Plus"],
    "Cadillac": ["CT4", "CT5", "Escalade", "XT4", "XT5", "XT6", "LYRIQ"],
    "Chevrolet": ["Spark", "Sonic", "Cruze", "Malibu", "Impala", "Camaro", "Corvette", "Trax", "Equinox", "Blazer", "Traverse", "Tahoe", "Suburban", "Colorado", "Silverado 1500"],
    "Chrysler": ["300", "Pacifica", "Voyager"],
    "Citroën": ["C1", "C3", "C4", "C5", "Berlingo", "C3 Aircross", "C5 Aircross"],
    "Dacia": ["Sandero", "Logan", "Duster", "Jogger", "Spring"],
    "Daewoo": ["Matiz", "Lanos", "Nubira", "Nexia", "Lacetti"],
    "Dodge": ["Challenger", "Charger", "Durango", "Grand Caravan", "Journey"],
    "Ferrari": ["Roma", "Portofino", "F8", "SF90", "812", "296 GTB", "Purosangue"],
    "Fiat": ["500", "Panda", "Punto", "Tipo", "500X", "500L"],
    "Ford": ["Fiesta", "Focus", "Mondeo", "Mustang", "Puma", "Kuga", "EcoSport", "Explorer", "Edge", "Ranger", "F-150", "Bronco", "Maverick"],
    "GAC": ["GS3", "GS4", "GS5", "GS8", "Aion S", "Aion Y"],
    "Genesis": ["G70", "G80", "G90", "GV70", "GV80"],
    "GMC": ["Canyon", "Sierra 1500", "Terrain", "Acadia", "Yukon"],
    "Great Wall": ["Wingle", "Poer", "Tank 300", "Tank 500"],
    "Haval": ["H2", "H6", "H9", "Jolion", "F7"],
    "Honda": ["Jazz", "Civic", "Accord", "HR-V", "CR-V", "Pilot", "Passport", "Ridgeline", "Fit", "Legend"],
    "Hyundai": ["i10", "i20", "i30", "i40", "Elantra", "Sonata", "Accent", "Veloster", "Kona", "Tucson", "Santa Fe", "Palisade", "Ioniq", "Ioniq 5", "Ioniq 6"],
    "Infiniti": ["Q30", "Q50", "Q60", "Q70", "QX30", "QX50", "QX60", "QX80"],
    "Jaguar": ["XE", "XF", "XJ", "F-Type", "E-Pace", "F-Pace", "I-Pace"],
    "Jeep": ["Compass", "Renegade", "Cherokee", "Grand Cherokee", "Wrangler", "Gladiator"],
    "Kia": ["Picanto", "Rio", "Ceed", "Stinger", "Cerato", "Optima", "Sportage", "Niro", "Stonic", "Sorento", "Telluride", "EV6"],
    "Lamborghini": ["Huracán", "Urus", "Revuelto"],
    "Land Rover": ["Defender", "Discovery", "Discovery Sport", "Freelander", "Range Rover", "Range Rover Sport", "Range Rover Evoque", "Range Rover Velar"],
    "Lancia": ["Ypsilon", "Delta"],
    "Lexus": ["IS", "ES", "GS", "LS", "RC", "LC", "NX", "RX", "GX", "LX", "UX"],
    "Lincoln": ["Corsair", "Nautilus", "Aviator", "Navigator"],
    "Lotus": ["Elise", "Evora", "Exige", "Emira", "Eletre"],
    "Maserati": ["Ghibli", "Quattroporte", "GranTurismo", "Levante", "Grecale"],
    "Mazda": ["Mazda2", "Mazda3", "Mazda6", "CX-3", "CX-30", "CX-5", "CX-60", "CX-9", "MX-5", "MX-30"],
    "McLaren": ["GT", "Artura", "720S", "750S", "Senna"],
    "Mercedes-Benz": ["A-Class", "B-Class", "C-Class", "E-Class", "S-Class", "CLA", "CLS", "GLA", "GLB", "GLC", "GLE", "GLS", "G-Class", "AMG GT", "EQA", "EQB", "EQC", "EQE", "EQS"],
    "MINI": ["Cooper", "Convertible", "Clubman", "Countryman", "Paceman", "Roadster"],
    "Mitsubishi": ["Mirage", "Lancer", "Eclipse Cross", "Outlander", "ASX", "Pajero", "L200"],
    "Nissan": ["Micra", "Juke", "Qashqai", "X-Trail", "Murano", "Pathfinder", "Navara", "Leaf", "Ariya", "GT-R", "370Z", "Altima", "Sentra", "Versa"],
    "Opel": ["Corsa", "Astra", "Insignia", "Crossland", "Grandland", "Mokka"],
    "Peugeot": ["108", "208", "308", "508", "2008", "3008", "5008"],
    "Pontiac": ["G6", "G8", "Solstice", "Firebird", "GTO"],
    "Porsche": ["911", "718 Boxster", "718 Cayman", "Cayenne", "Macan", "Panamera", "Taycan"],
    "RAM": ["1500", "2500", "3500", "ProMaster"],
    "Renault": ["Clio", "Megane", "Laguna", "Kadjar", "Captur", "Koleos", "Arkana", "Zoe"],
    "Rolls-Royce": ["Ghost", "Phantom", "Wraith", "Dawn", "Cullinan", "Spectre"],
    "SEAT": ["Ibiza", "Leon", "Arona", "Ateca", "Tarraco"],
    "Skoda": ["Fabia", "Rapid", "Octavia", "Superb", "Kamiq", "Karoq", "Kodiaq", "Enyaq"],
    "Smart": ["#1", "#3", "Fortwo", "Forfour"],
    "Subaru": ["Impreza", "Legacy", "Outback", "Forester", "XV", "BRZ", "WRX"],
    "Suzuki": ["Alto", "Swift", "Baleno", "Vitara", "S-Cross", "Jimny", "SX4"],
    "Tesla": ["Model S", "Model 3", "Model X", "Model Y", "Cybertruck", "Roadster"],
    "Toyota": ["Aygo", "Yaris", "Corolla", "Camry", "Avalon", "86", "Supra", "RAV4", "C-HR", "Prius", "Prius+", "Hilux", "Land Cruiser", "Land Cruiser Prado", "4Runner", "Tacoma", "Tundra", "Sequoia", "Highlander", "Venza", "Sienna", "bZ4X"],
    "Volkswagen": ["Polo", "Golf", "Passat", "Arteon", "T-Roc", "T-Cross", "Tiguan", "Touareg", "Touran", "ID.3", "ID.4", "ID.5", "ID.6", "Amarok"],
    "Volvo": ["S60", "S90", "V60", "V90", "XC40", "XC60", "XC90", "C40 Recharge"]
};

// Handle Map Toggle in Footer
document.addEventListener('DOMContentLoaded', function() {
    const mapToggles = document.querySelectorAll('.map-toggle');
    if (mapToggles.length > 0) {
        mapToggles.forEach(toggle => {
            toggle.addEventListener('click', function() {
                // Remove active styling from all
                mapToggles.forEach(btn => {
                    btn.classList.remove('active', 'text-dark');
                    btn.classList.add('text-secondary');
                    btn.style.backgroundColor = 'transparent';
                    btn.style.boxShadow = 'none';
                });
                
                // Add active styling to clicked
                this.classList.add('active', 'text-dark');
                this.classList.remove('text-secondary');
                this.style.backgroundColor = '#fff';
                this.style.boxShadow = '0 2px 4px rgba(0,0,0,0.05)';
                
                const target = this.getAttribute('data-target');
                
                // Toggle Maps
                const mapKorea = document.getElementById('mapKorea');
                const mapAze = document.getElementById('mapAze');
                const infoKorea = document.getElementById('infoKorea');
                const infoAze = document.getElementById('infoAze');
                
                if (target === 'korea') {
                    mapKorea.style.opacity = '1';
                    mapKorea.style.pointerEvents = 'auto';
                    mapAze.style.opacity = '0';
                    mapAze.style.pointerEvents = 'none';
                    
                    infoKorea.style.opacity = '1';
                    infoKorea.style.pointerEvents = 'auto';
                    infoAze.style.opacity = '0';
                    infoAze.style.pointerEvents = 'none';
                } else {
                    mapKorea.style.opacity = '0';
                    mapKorea.style.pointerEvents = 'none';
                    mapAze.style.opacity = '1';
                    mapAze.style.pointerEvents = 'auto';
                    
                    infoKorea.style.opacity = '0';
                    infoKorea.style.pointerEvents = 'none';
                    infoAze.style.opacity = '1';
                    infoAze.style.pointerEvents = 'auto';
                }
            });
        });
    }
});
