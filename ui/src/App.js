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
var id = 1;
var scheduleList = [];
var eventList = []
var addCourses = true;
const fetchData = async () => {
  try {
      const response = await fetch("http://127.0.0.1:8000");
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const result = await response.json();
      //console.log(result.schedule);
      scheduleList = result.schedule;
      console.log('The List', scheduleList);
      //setData(result);
  } catch (err) {
      console.log('Error', err);
  }
};

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
          //console.log('EVENT UPDATED', updatedEvent)
          updating(updatedEvent);
          updated = 1;
          //This callback will feed in the updatedEvent object
        },
        onEventClick(calendarEvent) {
          console.log('onEventClick', calendarEvent)
        },
        beforeRender() {
          fetchData();
        }
      },
  }, plugins)

  useEffect(() =>{
    calendar.eventsService.getAll();
  }, [])

  //WIP Function
  function updating(){
    if(typeof(calendar) != null && addCourses) {
      scheduleList.forEach(course => {

      
        var start_time = course["Start Time"];
        var end_time = course["End Time"];
        var title = course["Title"];
        var pattern = 'MWF'
        start_time = start_time.substring(0, start_time.length -2);
        end_time = end_time.substring(0, end_time.length -2);
        //If the second character is a colon, we need to alter the number
        var second_half;
        var first_num_start;
        var end_num_start;
        if(start_time.charAt(1) === ":") {
          second_half = start_time.substring(1);
          var start_first_num = parseInt(String(start_time.charAt(0)));
          if(start_first_num < 8) {
            start_first_num = start_first_num + 12;
            start_time = start_first_num + second_half;
          } else if(start_first_num < 10) {
            var newString = "0" + start_first_num;
            start_time = newString + second_half;
          }
        }
        if(end_time.charAt(1) === ":") {
          second_half = end_time.substring(1);
          var end_first_num = parseInt(String(end_time.charAt(0)));
          if(end_first_num < 8) {
            end_first_num = end_first_num + 12;
            console.log(end_first_num);
            end_time = end_first_num + second_half;
          } else if(end_first_num < 10) {
            var newString = "0" + end_first_num;
            end_time = newString + second_half;
          }
        }
        console.log('START TIME', start_time);
        console.log('END TIME', end_time);


        var start_date = '2024-11-18 ' + start_time
        var end_date = '2024-11-18 ' + end_time
        var rule = 'FREQ=WEEKLY;BYDAY=MO,WE,FR;UNTIL=20250101'
        if(course.Day == "Tuesday") {
          pattern = 'TTH'
          rule = 'FREQ=WEEKLY;BYDAY=TU,TH;UNTIL=20250101'
          start_date = '2024-11-19 ' + start_time
          end_date = '2024-11-19 ' + end_time
        }
        const theCourse = {
          id: id,
          title: title,
          start: start_date,
          end: end_date,
          rrule: rule,
        }
        try{
          calendar.events.add(theCourse);
          console.log('Added ', theCourse);
        } catch (e) {
          console.log('Could not add this course, ', theCourse);
        }
        id = id+1;
      })
      addCourses = false;
      
    }
  }

  
  return (
    <div>
      <div>
        <button onClick={updating}>Load Courses</button>
    </div>
      <div>
        <ScheduleXCalendar calendarApp={calendar} />
      </div>
    </div>
      
  )
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
export default App;
