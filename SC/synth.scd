// create a server object that will run on the local host using port #57110
m = Server(\cyclicalDance, NetAddr("127.0.0.1", 57110));
m.boot; //start the server

("***   The address of the server is: " + NetAddr.langPort + "   ***").postln;

(
SynthDef("sine", { arg freq=440;
    var osc;
    osc = SinOsc.ar(freq, 0, 0.1); // 800 Hz sine oscillator
    Out.ar(0, osc); // send output to audio bus zero.
}).add;
)

h = Synth( \sine );
NodeWatcher.register(h);

(
// define an echo effect
SynthDef("echo", { arg delay = 0.2, decay = 4;
    var in;
    in = In.ar(0,2);
    // use ReplaceOut to overwrite the previous contents of the bus.
    ReplaceOut.ar(0, CombN.ar(in, 0.5, delay, decay, 1, in));
}).add;
)

(
x = OSCFunc( { | msg, time, addr, port |

    var position = msg[1].asInteger;
    ( "position is " + position ).postln;
	switch(position,
		1, {
			echo_var = Synth(\echo);
			NodeWatcher.register(echo_var);
		}/*,
		2, {
			if (echo_var.isRunning,
				{ echo_var.free },
				{}
			);
		}*/
	);

}, "/handle" );
)

(
z = OSCFunc( { | msg, time, addr, port |
	m.freeAll;
}, "/reset" );
)

NodeWatcher.all

// Finish
m.freeAll;
m.quit; // quit the server