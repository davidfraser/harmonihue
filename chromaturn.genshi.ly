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

#(define rotation-mapping
  (list
{% for pitch_str, rotation in lilypond_pitch_rotations() %}
    (cons (ly:make-pitch ${pitch_str}) ${rotation})
{% end %}
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

#(define (pitch-to-rotation pitch)
  (let ((rotation (assoc pitch rotation-mapping pitch-equals?)))
    (if rotation
      (cdr rotation))))

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

{% if not lilypond_has_chromaturn() %}

chromaTurnOn = {
  \override NoteHead #'color = #color-notehead
  \override NoteHead #'stencil = #(lambda (grob)
    (let* ((note (ly:note-head::print grob))
           (rotation (pitch-to-rotation (ly:event-property (event-cause grob) 'pitch)))
           (combo-stencil (ly:stencil-add
               note
               (stencil-with-color
                   (ly:make-stencil (list 'embedded-ps
                        (string-append "gsave
                          currentpoint translate
                          newpath
                          0.75 0 translate
                          "
                          (ly:number->string rotation)
                          " rotate
                          -0.35 0.1 moveto
                          0.35 0.1 lineto
                          0.35 -0.1 lineto
                          -0.35 -0.1 lineto
                          closepath
                          fill
                          grestore" ))
                        (cons 0 1.3125)
                        (cons -.75 .75))
                   (x11-color 'white)))))
          (ly:make-stencil (ly:stencil-expr combo-stencil)
            (ly:stencil-extent note X)
            (ly:stencil-extent note Y))))
}

chromaTurnOff = {
  \revert NoteHead #'font-color
  \revert NoteHead #'stencil
}

{% end %}