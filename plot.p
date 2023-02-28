#Paint
        set terminal png size 900,500
        set title ARG2
        set output ARG1
        set datafile separator ","

        #x tics setting
        set xtics font "0,9"
        set xtics 600
        set xlabel "Epoch Time"
        set xdata time
        set timefmt "%s"
        set format x "%h"

        #y tics setting
        set ylabel "Destination IP Space"
        set yrange [3390656512:3390658559]

        plot ARG3 using 1:3 title "" with points pt 6 pointsize 0.3
