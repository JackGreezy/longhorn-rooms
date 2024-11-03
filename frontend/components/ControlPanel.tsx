interface ControlPanelProps {
  view: "map" | "list"
  setView: (view: "map" | "list") => void
}

export default function ControlPanel({ view, setView }: ControlPanelProps) {
  return (
    <div className="w-72 p-4 border-r border-gray-300">
      <h3 className="text-3xl font-semibold mb-4">Control Panel</h3>
      <button
        onClick={() => setView("map")}
        className={`w-full mb-2 px-4 py-2 text-white rounded ${view === "map" ? "bg-blue-600" : "bg-blue-400"}`}
      >
        Map View
      </button>
      <button
        onClick={() => setView("list")}
        className={`w-full px-4 py-2 text-white rounded ${view === "list" ? "bg-blue-600" : "bg-blue-400"}`}
      >
        List View
      </button>
    </div>
  )
}
