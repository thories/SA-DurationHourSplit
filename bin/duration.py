import datetime
import sys
from splunklib.searchcommands import dispatch, StreamingCommand, Configuration, Option, validators

@Configuration(local=True)
class DurationByHour(StreamingCommand):

    field_starttime = Option(require=True, validate=validators.Fieldname(),doc='''
    **Syntax:** **field=***<field>*
        **Description:** define column which contain current usage''')
    field_duration = Option(require=True, validate=validators.Fieldname(),doc='''
    **Syntax:** **field=***<field>*
        **Description:** define column which contain duration usage''')
    result = Option(require=False, validate=validators.Fieldname(),default="Epoch_Duration",doc='''
    **Syntax:** **result=***<result>*
        **Description:** define column name of result column''')

    def stream(self, events):
        for event in events:
            time_duration = self.durationByHour(int(event[self.field_starttime]), int(event[self.field_duration]))
            event[self.result] = time_duration
            yield event

    def durationByHour(self, field_starttime, field_duration):

        starttime = datetime.datetime.fromtimestamp(field_starttime)
        duration = datetime.timedelta(seconds=field_duration)
        endtime = starttime + duration
        current = starttime
        # Set next_current to the next hour-aligned datetime
        next_current = (starttime + datetime.timedelta(hours=1)).replace(minute=0, second=0)
        result = []
        if(next_current > endtime):
            time = str(next_current - datetime.timedelta(hours=1))
            duration = str(int((endtime-current).total_seconds()))
            result.append(time + '_' + duration)
        # Grab the start block (that ends on an hour alignment)
        # and then any full-hour blocks
        while next_current <= endtime:
            if(starttime==current):
                time = str(next_current - datetime.timedelta(hours=1))
            else:
                time = str(current)
            duration = str(int((next_current-current).total_seconds()))

            result.append(time + '_' + duration)
            # Advance both current and next_current to the following hour-aligned spots
            current = next_current
            if(next_current == endtime):
                break
            if((next_current + datetime.timedelta(hours=1)) > endtime):
                next_current = endtime
            else:
                next_current += datetime.timedelta(hours=1)
        return(result)

dispatch(DurationByHour, sys.argv, sys.stdin, sys.stdout, __name__)