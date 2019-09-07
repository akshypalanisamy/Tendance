package com.example.tendatesting;

public class Attendee {
    private String attendeeName, attendeeDuration, attendeeEndTime;

    public Attendee(String attendeeName, String attendeeDuration, String attendeeEndTime) {
        this.attendeeName = attendeeName;
        this.attendeeDuration = attendeeDuration;
        this.attendeeEndTime = attendeeEndTime;
    }

    public String getAttendeeName() {

        return attendeeName;
    }
    public void setAttendeeName(String attendeeName) {

        this.attendeeName = attendeeName;
    }
    public String getAttendeeDuration() {

        return attendeeDuration;
    }
    public void setAttendeeDuration(String attendeeDuration) {
        this.attendeeDuration = attendeeDuration;
    }
    public String getAttendeeEndTime() {

        return attendeeEndTime;
    }
    public void setAttendeeEndTime(String attendeeEndTime) {
        this.attendeeEndTime = attendeeEndTime;
    }


}
