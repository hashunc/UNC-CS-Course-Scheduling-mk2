import logo from './logo.svg';
import './App.css';
import React, { StrictMode, useEffect } from "react";
import ReactDOM from "react-dom";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { ScheduleXCalendar, useCalendarApp } from '@schedule-x/react';
import Calendar from './Calendar.tsx';
import {
  createViewDay,
  createViewMonthAgenda,
  createViewMonthGrid,
  createViewWeek,
  createCalendar
} from '@schedule-x/calendar'
import { createEventsServicePlugin } from '@schedule-x/events-service'
import '@schedule-x/theme-default/dist/index.css'
import { createDragAndDropPlugin } from '@schedule-x/drag-and-drop';
import { createEventRecurrencePlugin } from "@schedule-x/event-recurrence";
//const eventService = createEventsServicePlugin();
var updated = 0;
var eventList = [
  {
    id: 123,
    title: 'MWF',
    start: '2024-10-21 08:00',
    end: '2024-10-21 08:50',
    rrule: 'FREQ=WEEKLY;BYDAY=MO,WE,FR;UNTIL=20250101'
  },
  {
    id: 2,
    title: 'TTH',
    start: '2024-10-22 08:00',
    end: '2024-10-22 09:15',
    rrule: 'FREQ=WEEKLY;BYDAY=TU,TH;UNTIL=20250101'
  }
]

function App() {
  const plugins = [
    createEventsServicePlugin(),
    createDragAndDropPlugin(),
    createEventRecurrencePlugin()
]
    const calendar = useCalendarApp({
      views: [createViewDay(), createViewWeek(), createViewMonthGrid(), createViewMonthAgenda()],
      events: eventList,
      callbacks: {
        onEventUpdate(updatedEvent) {
          console.log('EVENT UPDATED', updatedEvent)
          updating();
          updated = 1;
          //This callback will feed in the updatedEvent object
        },
        onEventClick(calendarEvent) {
          console.log('onEventClick', calendarEvent)
        },
      },
  }, plugins)

  useEffect(() =>{
    calendar.eventsService.getAll();
  }, [])


  //WIP Function
  function updating(){
    if(typeof(calendar) != null) {
      console.log("UPDATING");
    }
  }

  
  return (
      <div>
        <ScheduleXCalendar calendarApp={calendar} />
      </div>
  )
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
export default App;
