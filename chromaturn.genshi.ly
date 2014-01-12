{% python
from chromaturn import *
from spectrum import *
%}
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
{% for pitch_str, color in lilypond_pitch_colors() %}{% with rgb=color.convert_to('rgb') %}
    (cons (ly:make-pitch ${pitch_str})	(rgb-color ${rgb.rgb_r/255.} ${rgb.rgb_g/255.} ${rgb.rgb_b/255.}))
{% end %}{% end %}
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

chromaNotesOn = {
  \override NoteHead #'color = #color-notehead
}

{% if lilypond_has_chromaturn() %}

% brew_chromaturn_stencil is a modified form of brew_ez_stencil from easyHeadsOn
% TODO: make this draw lines instead of using letters, and add intelligence for different note types
% FIXME: this makes sharps and flats overlay the notes
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

{% end %}

