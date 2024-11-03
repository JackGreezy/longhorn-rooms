import React, { useState } from "react"

const Sidebar: React.FC = () => {
  const [timeRange, setTimeRange] = useState<[number, number]>([0, 24])
  const handleTimeRangeChange = (e: React.ChangeEvent<HTMLInputElement>, index: number) => {
    const value = Number(e.target.value)
    setTimeRange((prevRange) => {
      const newRange = [...prevRange] as [number, number]
      newRange[index] = value
      if (newRange[0] > newRange[1]) {
        newRange[index === 0 ? 1 : 0] = value
      }
      return newRange
    })
  }
  return (
    <div className="sidebar">
      <div className="header">
        <button className="view-button">Map View</button>
        <button className="view-button">List View</button>
      </div>
      <div className="sliders">
        <label htmlFor="time-range">Select Time Range</label>
        <input
          type="range"
          id="time-range-start"
          min="0"
          max="24"
          value={timeRange[0]}
          onChange={(e) => handleTimeRangeChange(e, 0)}
        />
        <input
          type="range"
          id="time-range-end"
          min={timeRange[0]}
          max="24"
          value={timeRange[1]}
          onChange={(e) => handleTimeRangeChange(e, 1)}
        />
        <div className="time-values">
          <span>Start: {timeRange[0]}:00</span> - <span>End: {timeRange[1]}:00</span>
        </div>
      </div>
      <div className="chatbot-prompt">
        <button className="chat-button">Don't know where to study? Ask our Chat Bot</button>
      </div>
    </div>
  )
}
export default Sidebar
