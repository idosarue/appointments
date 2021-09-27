from therapist.models import Day
from therapist.forms import ContactFormEmailPatient
def day_processor(request):
    days = Day.disabled_days()          
    return {'day': days}


def form_proccesor(request):
    contact_form = ContactFormEmailPatient()
    return {'contact_form': contact_form}

def modal_proccesor(request):
    therapist_contact_patient_modal = '''
        <div class="modal fade" id="ContactModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog" role="document">
            <div class="modal-content">
                <div class="modal-header">
                <h5 class="modal-title">Send Email</h5>
                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                </button>
                </div>
                <div class="modal-body">
                <form id="contact-form-therapist" class="form" action="{% url 'send_contact_email' %}" method="POST"> 
                    {% csrf_token %}
                    {{contact_form.as_p}}
                    </div>
                    <div id="contact-result">
                    </div>
                    <div class="modal-footer">
                        <button type="submit" class="btn btn-primary">Save changes</button>
                        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                    </form>
                </div>
            </div>
        </div>
    </div>        
    '''
    return {'therapist_contact_patient_modal': therapist_contact_patient_modal}