import { useCalendarApp, ScheduleXCalendar } from '@schedule-x/react'
import {
  createViewDay,
  createViewMonthAgenda,
  createViewMonthGrid,
  createViewWeek,
} from '@schedule-x/calendar'
import { createEventsServicePlugin } from '@schedule-x/events-service'
import '@schedule-x/theme-default/dist/index.css'
import { createDragAndDropPlugin } from '@schedule-x/drag-and-drop';
import { createEventRecurrencePlugin } from "@schedule-x/event-recurrence";
import React from 'react';
const eventService = createEventsServicePlugin();

function Calendar() {
    //const plugins = [createEventsServicePlugin()]
    var calendar;
    calendar = useCalendarApp({
        views: [createViewDay(), createViewWeek(), createViewMonthGrid(), createViewMonthAgenda()],
        events: [
        {
            id: 123,
            title: 'MWF',
            start: '2024-10-21 08:00',
            end: '2024-10-21 08:50',
            rrule: 'FREQ=WEEKLY;INTERVAL=2;BYDAY=MO,WE,FR;UNTIL=20250101'
        },
        {
            id: 2,
            title: 'TTH',
            start: '2024-10-22 08:00',
            end: '2024-10-22 09:15',
            rrule: 'FREQ=WEEKLY;INTERVAL=2;BYDAY=TU,TH;UNTIL=20250101'
        }
        ],
        plugins: [
            eventService,
            createDragAndDropPlugin(),
            createEventRecurrencePlugin()
        ]
    });
    console.log(eventService);
    calendar.render(document.getElementById('calendar')!);
    return (
        <div>
          <ScheduleXCalendar calendarApp={calendar} />
        </div>
    )
}
export default Calendar;