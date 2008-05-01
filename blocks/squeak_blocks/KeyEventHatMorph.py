'From MIT Squeak 0.9.4 (June 1, 2003) [No updates present.] on 30 April 2008 at 1:48:15 pm'!EventHatMorph subclass: #KeyEventHatMorph	instanceVariableNames: ''	classVariableNames: ''	poolDictionaries: ''	category: 'Scratch-Blocks'!!KeyEventHatMorph commentStamp: 'jm 3/28/2005 12:26' prior: 0!I am a hat block for stacks triggered by Scratch keyboard events.!!KeyEventHatMorph methodsFor: 'initialization' stamp: 'ee 11/10/2007 18:13'!initialize	| parts s |	super initialize.	self removeAllMorphs.	parts _ ScratchTranslator labelPartsFor: 'when %k key pressed'.	s _ StringMorph new contents: parts first; font: LabelFont; color: Color white.	self addMorphBack: s.	scriptNameMorph _ ChoiceArgMorph new		getOptionsSelector: #keyNames;		options: ScriptableScratchMorph new keyNames;		choice: 'space' localized.	self addMorphBack: scriptNameMorph.	s _ s fullCopy contents: parts second.	self addMorphBack: s.! !!KeyEventHatMorph methodsFor: 'other' stamp: 'jm 3/28/2005 12:40'!asBlockTuple	"Answer a tuple (Array) describing this block and its arguments."	^ Array		with: self class name		with: scriptNameMorph choice! !!KeyEventHatMorph methodsFor: 'other' stamp: 'jm 3/26/2005 21:00'!choice: aString	scriptNameMorph choice: aString.! !!KeyEventHatMorph methodsFor: 'other' stamp: 'jm 3/28/2005 12:38'!eventName	^ 'Scratch-KeyPressedEvent'! !!KeyEventHatMorph methodsFor: 'other' stamp: 'jm 12/8/2005 19:22'!printHatNameOn: aStream	"Append a human-readable string for this hat block's name to the given stream."	aStream nextPutAll: 'when ', scriptNameMorph choice, ' key pressed'; cr.! !!KeyEventHatMorph methodsFor: 'other' stamp: 'jm 8/9/2007 20:03'!respondsToKeyEvent: aMorphicKeyEvent	| evtAscii |	evtAscii _ aMorphicKeyEvent keyCharacter asLowercase asciiValue.	evtAscii = Character enter asciiValue ifTrue: [		evtAscii _ Character cr asciiValue].	^ evtAscii = (ScriptableScratchMorph new asciiFor: scriptNameMorph choice asString)! !