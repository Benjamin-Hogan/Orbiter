Orbiter V1
An open-source astrodynamics sandbox for students, hobbyists, and aspiring engineers.

🚀 Overview
Orbiter V1 is a lightweight, modular software project that enables users to explore, visualize, and simulate orbital mechanics intuitively — whether they have no prior experience or advanced astrodynamics knowledge.
It is engineered to run efficiently on low-spec systems (e.g., Raspberry Pi, old laptops) and is designed around SI units to encourage scientific rigor.

This project aims to make real astrodynamics accessible and educational without sacrificing technical integrity.

📜 Project Goals
Educational: Make orbital mechanics concepts intuitive for complete beginners.

Professional-grade: Offer depth and modularity to support advanced custom simulations.

Lightweight: Prioritize performance for low-end hardware (efficient CPU, RAM, GPU usage).

Transparent: SI units, open data, and clear physics throughout.

Extendable: Designed with future add-ons like n-body simulation, mission planning tools, and scripting in mind.

🎯 Target Audience
Students learning about orbits for the first time

Hobbyists and DIY engineers

University and high school programs

Anyone interested in spaceflight dynamics

🛠️ Core Components

Component	Description
Frontend	A minimal, responsive GUI for orbit visualization, control panels, and tutorials
Backend	Physics engine calculating orbital mechanics, forces, maneuvers
Data	Standardized input (JSON/YAML) for spacecraft, celestial bodies
Simulations	Pre-built scenarios (Hohmann transfers, plane changes, rendezvous, etc.)
📦 System Requirements
Python 3.11+ (core engine)

Lightweight front-end framework (Tkinter, PyQt, or browser-based UI)

OpenGL (for 3D visualization) (optional, depending on device capacity)

RAM: 512MB minimum

CPU: 1GHz single-core minimum

We aim to allow running a basic simulation on a Raspberry Pi Zero 2 W.

📐 Design Philosophy
SI Units Only (meters, seconds, kilograms, radians)

No Unnecessary Dependencies — runs "bare-metal" whenever possible

Explicit Physics — every assumption documented

Error Transparency — errors are surfaced clearly for educational value

🧠 Future Directions
Add scripting support (Python console inside app)

Multi-body gravity (basic patched conics first)

Solar radiation pressure and atmospheric drag modules

Save and share missions and spacecraft

Multiplayer simulation modes (cooperative mission design)

🤝 Contributing
We welcome community contributions!
Before submitting pull requests:

Keep simulations lightweight

Follow SI units rigorously

Prioritize clarity over cleverness in code

Document assumptions and sources for all physics models

Detailed contributing guidelines will be added soon.

📚 Resources and References
Curtis, Orbital Mechanics for Engineering Students

NASA SP-8021: Fundamentals of Astrodynamics

Vallado, Fundamentals of Astrodynamics and Applications

Open-source datasets for planetary ephemerides (NAIF SPICE Toolkit)

🛰️ License
Orbiter V1 is licensed under the MIT License.

