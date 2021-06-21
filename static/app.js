
const root = document.documentElement;

const fretboard = document.querySelector('.fretboard');
const numberOfFretsSelector = document.querySelector('#number-of-frets');
const toneJs = window.Tone;

let numberOfFrets = 17;
const numberOfStrings = 6;
const singleFretMarkPositions = [3, 5, 7, 9, 15, 17, 19, 21];
const doubleFretMarkPositions = [12, 24];

const notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"];
const guitarTunings = [4, 11, 7, 2, 9, 4]; // standard e tuning

const app = {
    init(){
        this.setupFretboard();
        this.setupEventListeners();
    },
    setupFretboard(){
        fretboard.innerHTML = "";
        root.style.setProperty('--number-of-strings', numberOfStrings);

        // add strings
        for (let i =0; i < numberOfStrings; i++){
            let string = tools.createElement('div');
            string.classList.add('string');
            fretboard.appendChild(string);

            // add frets
            for (let fret = 0; fret <= numberOfFrets; fret++){
                let noteFret = tools.createElement('div');
                noteFret.classList.add('note-fret');
                string.appendChild(noteFret);

                let noteName = this.generateNoteNames(fret + guitarTunings[i])
                noteFret.setAttribute('data-note', noteName);

                // add single fretmarks
                if (i == 0 && singleFretMarkPositions.includes(fret)){
                    noteFret.classList.add('single-fretmark');
                }

                // add double fretmarks
                if (i == 0 && doubleFretMarkPositions.includes(fret)){
                    let doubleFretMark = tools.createElement('div');
                    doubleFretMark.classList.add('double-fretmark');
                    noteFret.appendChild(doubleFretMark);
                }
            }
        }
    },
    generateNoteNames(noteIndex){
        noteIndex = noteIndex % 12;
        noteName = notes[noteIndex];
        return noteName;
    },
    setupEventListeners(){
        fretboard.addEventListener('mouseover', (event) => {
            if (event.target.classList.contains('note-fret')){
                event.target.style.setProperty('--noteDotOpacity', 0.5);

                let note = $(event.srcElement).attr("data-note");

                // play sound
                let now = Tone.now()
                let synth = new Tone.Synth().toDestination();
                synth.triggerAttackRelease(`${note}4`, "8n", now + 0.2);
                synth.unsync();
            }
        })
        fretboard.addEventListener('mouseout', (event) => {
            event.target.style.setProperty('--noteDotOpacity', 0);
        })
        numberOfFretsSelector.addEventListener('change', (event) => {
            numberOfFrets = numberOfFretsSelector.value;
            this.setupFretboard();
        })


    }
}

const tools = {
    createElement(element, content){
        element = document.createElement(element);
        if (content){
            element.innerHTML = content;
        }
        return element;
    }
}


app.init();