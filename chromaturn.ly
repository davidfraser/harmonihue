%% This file is in the public domain.
\version "2.12.3"

\header {
  lsrtags = "pitches, editorial-annotations"

  texidoc = "
It is possible to color note heads depending on their pitch and/or
their names: the function used in this example even makes it possible
to distinguish enharmonics. 

"
  doctitle = "Coloring notes depending on their pitch"
} % begin verbatim

%Association list of pitches to colors.
%TODO: handle double-sharps, double-flats, etc
#(define color-mapping
  (list
    (cons (ly:make-pitch 0 0 0)    (rgb-color 0.8 0.8 0.0)) 
    (cons (ly:make-pitch 0 0 1/2)  (rgb-color 0.0 0.4 0.8)) 
    (cons (ly:make-pitch 0 1 -1/2) (rgb-color 0.0 0.4 0.8)) 
    (cons (ly:make-pitch 0 1 0)    (rgb-color 0.8 0.0 0.0)) 
    (cons (ly:make-pitch 0 1 1/2)  (rgb-color 0.0 0.8 0.4)) 
    (cons (ly:make-pitch 0 2 -1/2) (rgb-color 0.0 0.8 0.4)) 
    (cons (ly:make-pitch 0 2 0)    (rgb-color 0.8 0.0 0.8)) 
    (cons (ly:make-pitch 0 3 -1/2) (rgb-color 0.8 0.0 0.8)) 
    (cons (ly:make-pitch 0 3 0)    (rgb-color 0.4 0.8 0.0)) 
    (cons (ly:make-pitch 0 2 1/2)  (rgb-color 0.4 0.8 0.0)) 
    (cons (ly:make-pitch 0 3 1/2)  (rgb-color 0.0 0.0 0.8)) 
    (cons (ly:make-pitch 0 4 -1/2) (rgb-color 0.0 0.0 0.8)) 
    (cons (ly:make-pitch 0 4 0)    (rgb-color 0.8 0.4 0.0)) 
    (cons (ly:make-pitch 0 4 1/2)  (rgb-color 0.0 0.8 0.8)) 
    (cons (ly:make-pitch 0 5 -1/2) (rgb-color 0.0 0.8 0.8)) 
    (cons (ly:make-pitch 0 5 0)    (rgb-color 0.8 0.0 0.4)) 
    (cons (ly:make-pitch 0 5 1/2)  (rgb-color 0.0 0.8 0.0)) 
    (cons (ly:make-pitch 0 6 -1/2) (rgb-color 0.0 0.8 0.0)) 
    (cons (ly:make-pitch 0 6 0)    (rgb-color 0.4 0.0 0.8)) 
    (cons (ly:make-pitch 1 0 -1/2) (rgb-color 0.4 0.0 0.8)) 
    (cons (ly:make-pitch 0 6 1/2)  (rgb-color 0.8 0.8 0.0)) 
  )
 )

%Compare pitch and alteration (not octave).
#(define (pitch-equals? p1 p2)
  (and
    (= (ly:pitch-alteration p1) (ly:pitch-alteration p2))
    (= (ly:pitch-notename p1) (ly:pitch-notename p2))))

#(define (pitch-to-color pitch)
  (let ((color (assoc pitch color-mapping pitch-equals?)))
    (if color
      (cdr color))))

#(define (color-notehead grob)
  (pitch-to-color
    (ly:event-property (event-cause grob) 'pitch)))

% brew_chromaturn_stencil is a modified form of brew_ez_stencil from easyHeadsOn
% TODO: make this draw lines instead of using letters, and add intelligence for different note types
chromaTurnOn = {
  \override NoteHead #'color = #color-notehead
  \override NoteHead #'stencil = #ly:note-head::brew-chromaturn-stencil
  \override NoteHead #'font-size = #-7
  \override NoteHead #'font-family = #'sans
  \override NoteHead #'font-series = #'bold
}

chromaTurnOff = {
  \revert NoteHead #'font-color
  \revert NoteHead #'stencil
  \revert NoteHead #'font-size
  \revert NoteHead #'font-family
  \revert NoteHead #'font-series
  \revert NoteHead #'note-names
}




