"use client";

import React, { useState, useEffect } from "react";
import { Phone, PhoneOff, Volume2, Mic, Grid, Info } from "lucide-react";
import { Button, Card } from "@/components/ui";

export default function IVRDemo() {
  const [isCalling, setIsCalling] = useState(false);
  const [callStatus, setCallStatus] = useState("Incoming Call...");
  const [step, setStep] = useState(0); // 0: Idle, 1: Incoming, 2: Active Call

  const simulateCall = () => {
    setStep(1);
    const ringtone = new Audio("/ringtone.mp3"); // Optional
    // setIsCalling(true);
  };

  const answerCall = () => {
    setStep(2);
    setCallStatus("00:01");
  };

  const endCall = () => {
    setStep(0);
    setCallStatus("Incoming Call...");
  };

  return (
    <div className="min-h-screen bg-gray-900 flex flex-col items-center justify-center p-6 font-sans">
      <div className="max-w-4xl w-full grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
        
        {/* Left Side: The Simulation */}
        <div className="flex justify-center">
          <div className="relative w-72 h-[550px] bg-gray-800 rounded-[40px] border-[8px] border-gray-700 shadow-2xl overflow-hidden flex flex-col">
            
            {/* Speaker Hole */}
            <div className="h-6 flex justify-center items-center">
              <div className="w-12 h-1 bg-gray-700 rounded-full" />
            </div>

            {/* Screen Area */}
            <div className="flex-1 bg-blue-50 m-4 rounded-xl overflow-hidden flex flex-col border-2 border-gray-600">
              {step === 0 ? (
                <div className="flex-1 flex flex-col items-center justify-center p-4 text-center">
                  <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mb-4">
                    <Phone className="text-blue-600" />
                  </div>
                  <h3 className="text-gray-900 font-bold text-lg">Keypad Phone</h3>
                  <p className="text-gray-500 text-sm">Waiting for reminder...</p>
                  <Button 
                    onClick={simulateCall}
                    className="mt-6 bg-blue-600 hover:bg-blue-700 text-white rounded-full px-6"
                  >
                    Trigger Reminder
                  </Button>
                </div>
              ) : step === 1 ? (
                <div className="flex-1 flex flex-col items-center justify-between p-6 bg-blue-600 text-white animate-pulse">
                  <div className="mt-8 text-center">
                    <p className="text-blue-100 text-sm uppercase tracking-widest mb-2">Incoming Call</p>
                    <h2 className="text-2xl font-bold italic tracking-tighter">CARA HEALTH</h2>
                  </div>
                  <div className="flex gap-8 mb-4 w-full">
                    <button onClick={answerCall} className="flex-1 bg-green-500 p-4 rounded-xl flex items-center justify-center">
                      <Phone className="w-8 h-8" />
                    </button>
                    <button onClick={endCall} className="flex-1 bg-red-500 p-4 rounded-xl flex items-center justify-center">
                      <PhoneOff className="w-8 h-8" />
                    </button>
                  </div>
                </div>
              ) : (
                <div className="flex-1 flex flex-col items-center justify-between p-6 bg-white">
                  <div className="mt-8 text-center">
                    <Volume2 className="w-8 h-8 text-blue-600 mb-2 mx-auto animate-bounce" />
                    <h2 className="text-xl font-bold text-gray-900">CARA HEALTH</h2>
                    <p className="text-blue-600 font-mono mt-2">{callStatus}</p>
                  </div>
                  
                  <div className="w-full space-y-4">
                    <div className="bg-gray-100 p-4 rounded-xl text-center border-2 border-dashed border-gray-300">
                      <p className="text-sm text-gray-600 italic">
                        "Hello! It is time for your Metformin. Press 1 if taken."
                      </p>
                    </div>
                    
                    {/* Simulated Keypad for user interaction */}
                    <div className="grid grid-cols-3 gap-2">
                      {[1, 2, 3, 4, 5, 6, 7, 8, 9, "*", 0, "#"].map((num) => (
                        <button 
                          key={num}
                          onClick={() => {
                            if (num === 1) setCallStatus("Medication Logged!");
                            if (num === 1) setTimeout(endCall, 2000);
                          }}
                          className="h-10 bg-gray-200 hover:bg-gray-300 rounded-lg flex items-center justify-center font-bold text-gray-700 active:scale-95 transition-all"
                        >
                          {num}
                        </button>
                      ))}
                    </div>

                    <button onClick={endCall} className="w-full bg-red-500 text-white p-3 rounded-xl font-bold">
                      End Call
                    </button>
                  </div>
                </div>
              )}
            </div>

            {/* Physical Keypad Simulation (Non-Functional, Visual) */}
            <div className="p-6 grid grid-cols-3 gap-3 bg-gray-800 rounded-b-[40px]">
               <div className="h-8 bg-gray-700 rounded-lg" />
               <div className="h-8 bg-gray-600 rounded-full border-2 border-gray-500" />
               <div className="h-8 bg-gray-700 rounded-lg" />
               {[...Array(9)].map((_, i) => (
                 <div key={i} className="h-10 bg-gray-700 rounded-xl flex items-center justify-center text-gray-500 font-bold text-xs">
                   {i + 1}
                 </div>
               ))}
            </div>
          </div>
        </div>

        {/* Right Side: Educational Content */}
        <div className="text-white space-y-8">
          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1 bg-blue-600/20 text-blue-400 rounded-full text-sm font-medium mb-4">
              <Mic className="w-4 h-4" />
              IVR Voice Reminders
            </div>
            <h1 className="text-4xl font-bold mb-4 bg-gradient-to-r from-white to-gray-400 bg-clip-text text-transparent">
              Closing the Tech Gap for Elders
            </h1>
            <p className="text-gray-400 text-lg leading-relaxed">
              Not every patient has a smartphone or high-speed internet. Our IVR (Interactive Voice Response) system ensures that even users with simple keypad phones never miss a dose.
            </p>
          </div>

          <div className="grid grid-cols-1 gap-4">
            <FeatureCard 
              icon={<Phone className="text-green-400" />}
              title="Automated Call Trigger"
              desc="If a dose is missed by 30 mins, a call is automatically placed to the patient's registered number."
            />
            <FeatureCard 
              icon={<Volume2 className="text-indigo-400" />}
              title="Natural Voice Guidance"
              desc="Uses high-quality Text-to-Speech to provide clear instructions in the patient's preferred local language."
            />
            <FeatureCard 
              icon={<Grid className="text-blue-400" />}
              title="Keypad Feedback"
              desc="Patients press simple keys (1, 2) to log their adherence. No apps, no typing, no complexity."
            />
          </div>

          <div className="p-6 bg-gray-800/50 rounded-3xl border border-gray-700">
             <div className="flex items-start gap-4">
               <div className="p-2 bg-blue-600 rounded-lg">
                 <Info className="text-white w-5 h-5" />
               </div>
               <div>
                 <h4 className="font-bold text-white mb-1">Developer Note</h4>
                 <p className="text-sm text-gray-400">
                   This demo simulates the integration with <strong>Exotel</strong>. In production, we use a webhook to catch the DTMF (keypad) input and update the <code>adherence_logs</code> table in real-time.
                 </p>
               </div>
             </div>
          </div>
        </div>

      </div>
    </div>
  );
}

function FeatureCard({ icon, title, desc }: { icon: React.ReactNode, title: string, desc: string }) {
  return (
    <Card className="p-6 bg-gray-800/30 border-gray-700 flex items-start gap-4 hover:bg-gray-800/50 transition-colors">
      <div className="p-3 bg-gray-900 rounded-2xl">{icon}</div>
      <div>
        <h3 className="font-bold text-white mb-1">{title}</h3>
        <p className="text-sm text-gray-500">{desc}</p>
      </div>
    </Card>
  );
}
