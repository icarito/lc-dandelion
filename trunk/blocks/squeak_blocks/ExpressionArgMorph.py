'From MIT Squeak 0.9.4 (June 1, 2003) [No updates present.] on 30 April 2008 at 1:48:00 pm'!ArgMorph subclass: #ExpressionArgMorph	instanceVariableNames: 'isNumber '	classVariableNames: ''	poolDictionaries: ''	category: 'Scratch-Blocks'!!ExpressionArgMorph commentStamp: 'jm 6/21/2004 13:29' prior: 0!I represent a literal value such as a number or string. I can be edited.!!ExpressionArgMorph methodsFor: 'initialization' stamp: 'jm 6/22/2007 12:49'!initialize	super initialize.	isNumber _ true.	self borderWidth: 1.	self borderInset.	self color: (Color gray: 0.95).	self extent: 25@12.	"To allow for editing in place."	labelMorph _ StringFieldMorph new		font: BlockMorph argFont;		borderWidth: 0;		stringInset: 5@0;		doResizing: true;		color: Color transparent.	self addMorph: labelMorph.	self numExpression: '10'.! !!ExpressionArgMorph methodsFor: 'accessing' stamp: 'jm 7/4/2004 12:38'!defaultValue: anObject	anObject isNumber ifTrue: [self numExpression: anObject].	(anObject isKindOf: String) ifTrue: [self stringExpression: anObject].	'-' = anObject ifTrue: [self numExpression: ' '].  "blank, evaluates to zero"! !!ExpressionArgMorph methodsFor: 'accessing' stamp: 'jm 10/26/2007 22:00'!numExpression: aNumber	isNumber _ true.	self height: 12.	labelMorph		isNumeric: true;		height: 13;		position: self position.	aNumber isFloat		ifTrue: [labelMorph contents: aNumber printStringNoExponent]		ifFalse: [labelMorph contents: aNumber asString].	self fixArgLayout.! !!ExpressionArgMorph methodsFor: 'accessing' stamp: 'jm 12/31/2005 10:50'!stringExpression: aString	isNumber _ false.	self height: 15.	labelMorph		isNumeric: false;		height: 14;		position: self position + (0@1).	labelMorph contents: aString.	self fixArgLayout.! !!ExpressionArgMorph methodsFor: 'queries' stamp: 'jm 7/7/2004 00:24'!acceptsDroppedReporters	^ true! !!ExpressionArgMorph methodsFor: 'queries' stamp: 'jm 11/28/2006 13:14'!acceptsTypeOf: aBlockMorph	"Answer true if I can accept a dropped reporter of the given type."	aBlockMorph isReporter ifFalse: [^ false].	^ isNumber not or: [aBlockMorph isBooleanReporter not]! !!ExpressionArgMorph methodsFor: 'drawing' stamp: 'jm 3/29/2005 20:18'!drawOn: aCanvas 	| darkerC right topY bottomY radius xInset c |	isNumber ifFalse: [^ super drawOn: aCanvas].	darkerC _ Color gray.	right _ self width.	topY _ bottomY _ radius _ self height // 2.	self height even ifTrue: [topY _ bottomY - 1].	[topY >= 0] whileTrue: [		xInset _ radius - (radius squared - (radius - topY - 1) squared) sqrt rounded.		self drawHLineFrom: xInset to: (xInset + 1) y: topY color: darkerC on: aCanvas.		c _ (topY < 1) ifTrue: [darkerC] ifFalse: [Color white].		self drawHLineFrom: xInset + 1 to: right - (xInset + 1) y: topY color: c on: aCanvas.		self drawHLineFrom: (right - (xInset + 1)) to: (right - xInset) y: topY color: darkerC on: aCanvas.		self drawHLineFrom: xInset to: right - xInset y: bottomY color: Color white on: aCanvas.		xInset = 0 ifTrue: [			self drawHLineFrom: xInset + 1 to: xInset + 2 y: topY color: Color white on: aCanvas.			self drawHLineFrom: xInset to: xInset + 1 y: bottomY color: darkerC on: aCanvas.			self drawHLineFrom: (right - (xInset + 1)) to: (right - xInset) y: bottomY color: darkerC on: aCanvas].		bottomY _ bottomY + 1.		topY _ topY - 1].! !!ExpressionArgMorph methodsFor: 'drawing' stamp: 'jm 3/28/2005 17:12'!isRectangular	^ isNumber not! !!ExpressionArgMorph methodsFor: 'evaluation' stamp: 'jm 7/1/2004 12:03'!evaluate	"Answer the result of evaluating my expression in the context of the given ScratchProcess."	| expr |	expr _ labelMorph contents.	isNumber		ifTrue: [^ expr asNumberNoError]		ifFalse: [^ expr].  "string"! !!ExpressionArgMorph methodsFor: 'object i/o' stamp: 'jm 9/24/2003 18:19'!fieldsVersion	^ 1! !!ExpressionArgMorph methodsFor: 'object i/o' stamp: 'jm 6/21/2004 17:57'!initFieldsFrom: anObjStream version: classVersion	super initFieldsFrom: anObjStream version: classVersion.	self initFieldsNamed: #(		isNumber	) from: anObjStream.! !!ExpressionArgMorph methodsFor: 'object i/o' stamp: 'jm 6/21/2004 17:57'!storeFieldsOn: anObjStream	super storeFieldsOn: anObjStream.	self storeFieldsNamed: #(		isNumber	) on: anObjStream.! !!ExpressionArgMorph methodsFor: 'private' stamp: 'jm 12/31/2005 10:53'!fixArgLayout	self width: labelMorph width.! !