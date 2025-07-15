"use client"

import { useState } from "react"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"

export default function AirCombatAI() {
  const [activeTab, setActiveTab] = useState("mission")
  const [inputs, setInputs] = useState({
    mission: "",
    threat: "",
    debrief: "",
  })
  const [results, setResults] = useState({
    mission: "",
    threat: "",
    debrief: "",
  })
  const [loading, setLoading] = useState({
    mission: false,
    threat: false,
    debrief: false,
  })

  const handleSubmit = async (type: "mission" | "threat" | "debrief") => {
    setLoading((prev) => ({ ...prev, [type]: true }))

    const endpoints = {
      mission: "http://127.0.0.1:8000/plan",
      threat: "http://127.0.0.1:8000/advise",
      debrief: "http://127.0.0.1:8000/debrief",
    }

    try {
      const response = await fetch(endpoints[type], {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text: inputs[type] }), // <-- FIXED: `text` instead of `input`
      })
  
      if (response.ok) {
        const data = await response.json()
        setResults((prev) => ({ ...prev, [type]: data.result }))
      } else {
        setResults((prev) => ({
          ...prev,
          [type]: `Error: ${response.status} - ${response.statusText}`,
        }))
      }
    } catch (error) {
      setResults((prev) => ({
        ...prev,
        [type]: `Network Error: ${error instanceof Error ? error.message : "Unknown error"}`,
      }))
    } finally {
      setLoading((prev) => ({ ...prev, [type]: false }))
    }
  }

  const handleInputChange = (type: "mission" | "threat" | "debrief", value: string) => {
    setInputs((prev) => ({ ...prev, [type]: value }))
  }

  return (
    <div className="min-h-screen relative text-green-400 font-mono">
      {/* Background image */}
      <div
        className="absolute inset-0 bg-cover bg-center bg-no-repeat"
        style={{
          backgroundImage:
            "url('https://hebbkx1anhila5yf.public.blob.vercel-storage.com/2.jpg-wLXRmHkQDyYm8P3yaDZSJyc0PHlw1e.jpeg')",
        }}
      ></div>

      {/* Dark overlay for better text readability */}
      <div className="absolute inset-0 bg-black/60"></div>

      <div className="relative z-10 container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-2xl font-bold text-green-600/60 mb-2">Air Combat AI</h1>
        </div>

        {/* Main Interface */}
        <div className="max-w-4xl mx-auto">
          <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
            <TabsList className="grid w-full grid-cols-3 bg-slate-800/50 border border-green-500/30">
              <TabsTrigger
                value="mission"
                className="data-[state=active]:bg-green-500/20 data-[state=active]:text-green-300 text-green-400 border-r border-green-500/30"
              >
                MISSION PLANNER
              </TabsTrigger>
              <TabsTrigger
                value="threat"
                className="data-[state=active]:bg-green-500/20 data-[state=active]:text-green-300 text-green-400 border-r border-green-500/30"
              >
                THREAT ADVISOR
              </TabsTrigger>
              <TabsTrigger
                value="debrief"
                className="data-[state=active]:bg-green-500/20 data-[state=active]:text-green-300 text-green-400"
              >
                DEBRIEF ANALYZER
              </TabsTrigger>
            </TabsList>

            <TabsContent value="mission" className="mt-6">
              <div className="space-y-4">
                <div className="border border-green-500/30 bg-slate-900/50 p-4 rounded">
                  <h3 className="text-green-300 mb-3 text-sm font-bold">MISSION PARAMETERS INPUT</h3>
                  <Textarea
                    value={inputs.mission}
                    onChange={(e) => handleInputChange("mission", e.target.value)}
                    placeholder="Enter mission objectives, waypoints, and tactical requirements..."
                    className="min-h-32 bg-black/50 border-green-500/50 text-green-400 placeholder:text-green-600 font-mono text-sm resize-none"
                  />
                  <Button
                    onClick={() => handleSubmit("mission")}
                    disabled={loading.mission || !inputs.mission.trim()}
                    className="mt-3 bg-green-600/20 hover:bg-green-600/30 text-green-300 border border-green-500/50 font-mono text-sm"
                  >
                    {loading.mission ? "PROCESSING..." : "GENERATE PLAN"}
                  </Button>
                </div>

                {results.mission && (
                  <div className="border border-green-500/30 bg-slate-900/50 p-4 rounded">
                    <h3 className="text-green-300 mb-3 text-sm font-bold">TACTICAL ANALYSIS</h3>
                    <pre className="text-green-400 text-sm whitespace-pre-wrap font-mono">{results.mission}</pre>
                  </div>
                )}
              </div>
            </TabsContent>

            <TabsContent value="threat" className="mt-6">
              <div className="space-y-4">
                <div className="border border-green-500/30 bg-slate-900/50 p-4 rounded">
                  <h3 className="text-green-300 mb-3 text-sm font-bold">THREAT ASSESSMENT INPUT</h3>
                  <Textarea
                    value={inputs.threat}
                    onChange={(e) => handleInputChange("threat", e.target.value)}
                    placeholder="Describe enemy positions, capabilities, and environmental factors..."
                    className="min-h-32 bg-black/50 border-green-500/50 text-green-400 placeholder:text-green-600 font-mono text-sm resize-none"
                  />
                  <Button
                    onClick={() => handleSubmit("threat")}
                    disabled={loading.threat || !inputs.threat.trim()}
                    className="mt-3 bg-green-600/20 hover:bg-green-600/30 text-green-300 border border-green-500/50 font-mono text-sm"
                  >
                    {loading.threat ? "ANALYZING..." : "ASSESS THREATS"}
                  </Button>
                </div>

                {results.threat && (
                  <div className="border border-green-500/30 bg-slate-900/50 p-4 rounded">
                    <h3 className="text-green-300 mb-3 text-sm font-bold">THREAT ANALYSIS</h3>
                    <pre className="text-green-400 text-sm whitespace-pre-wrap font-mono">{results.threat}</pre>
                  </div>
                )}
              </div>
            </TabsContent>

            <TabsContent value="debrief" className="mt-6">
              <div className="space-y-4">
                <div className="border border-green-500/30 bg-slate-900/50 p-4 rounded">
                  <h3 className="text-green-300 mb-3 text-sm font-bold">MISSION DEBRIEF INPUT</h3>
                  <Textarea
                    value={inputs.debrief}
                    onChange={(e) => handleInputChange("debrief", e.target.value)}
                    placeholder="Enter mission results, performance data, and lessons learned..."
                    className="min-h-32 bg-black/50 border-green-500/50 text-green-400 placeholder:text-green-600 font-mono text-sm resize-none"
                  />
                  <Button
                    onClick={() => handleSubmit("debrief")}
                    disabled={loading.debrief || !inputs.debrief.trim()}
                    className="mt-3 bg-green-600/20 hover:bg-green-600/30 text-green-300 border border-green-500/50 font-mono text-sm"
                  >
                    {loading.debrief ? "ANALYZING..." : "ANALYZE DEBRIEF"}
                  </Button>
                </div>

                {results.debrief && (
                  <div className="border border-green-500/30 bg-slate-900/50 p-4 rounded">
                    <h3 className="text-green-300 mb-3 text-sm font-bold">PERFORMANCE ANALYSIS</h3>
                    <pre className="text-green-400 text-sm whitespace-pre-wrap font-mono">{results.debrief}</pre>
                  </div>
                )}
              </div>
            </TabsContent>
          </Tabs>
        </div>
      </div>
    </div>
  )
}
