
let current_page = null
let prev_page = null
let second_to_prev_page = null
let first_iteration = true
let url = "http://127.0.0.1:5000/end_point"

function search_in_tree(node, class_name){
    var found = false; 
    if (node.className == class_name){
        return true 
    }
    if (node.childNodes.length){
        for (var i=0; i<node.childNodes.length; ++i){
            childNode = node.childNodes[i]
            found = found || search_in_tree(childNode, class_name)
            if (found){
                return true;
            }
                
        }
        return found;
    }else{
        return false
    }

}

function send_request(end_point){
    if (end_point){
        xhttp = new XMLHttpRequest();
        var endpoint_url = url.replace(/end_point/g, end_point)
        xhttp.open("GET", endpoint_url);
        xhttp.send('')
    }   
}


// Select the node that will be observed for mutations
const targetNode = document.getElementById("root");

// Options for the observer (which mutations to observe)
const config = { attributes: true, childList: true, subtree: true };



const callback = (mutationList, observer) => {
  for (const mutation of mutationList) {
    if (mutation.addedNodes.length){
        for (var i=0; i<mutation.addedNodes.length;++i){
            addedNode = mutation.addedNodes[i]
            if (search_in_tree(addedNode,"ConfirmationScreen_container__WeW6O")) {
                current_page = 'confirmation-screen'
            }else if (search_in_tree(addedNode,"ToastsController_container__1CFV3")){
                current_page = 'login-screen'
            }else if (search_in_tree(addedNode, "sg-flex sg-flex--justify-content-center sg-flex--align-items-center Navigation_item__1jzzc Navigation_logout__1Qn6G")){
                current_page = 'waiting-screen'
            }else if (search_in_tree(addedNode, "Timer_container__217az")){
                current_page = 'session-screen'
            }                
            if (!(prev_page===current_page)){
                var endpoint = 'change_status'
                if(!prev_page){
                    switch(current_page){
                        case 'login-screen':
                            endpoint = 'end_shift';
                            break;
                        case 'waiting-screen':
                            endpoint = 'start_shift';
                            break;
                        default: 
                            endpoint = 'change_status';
                    }
                } else if((prev_page==='confirmation-screen')&&(current_page==='waiting-screen')){
                    endpoint = 'missed_session'
                } else if(((prev_page==='waiting-screen')&&(current_page==='confirmation-screen'))
                  ||((prev_page==='waiting-screen')&&(current_page==='session-screen'))
                  ||((prev_page==='session-screen')&&(current_page==='waiting-screen')&&(second_to_prev_page!='confirmation-screen'))){
                    endpoint = ''
                }
                console.log('Second to previous:', second_to_prev_page)
                console.log('Previous page:', prev_page)
                console.log('Current page:', current_page)
                console.log('------------------')
                if(first_iteration){
                    first_iteration = false
                } else {
                    second_to_prev_page = prev_page
                }
                prev_page = current_page                
                send_request(endpoint)
                break;
            }
        }
    }  
  }
};

// Create an observer instance linked to the callback function
const observer = new MutationObserver(callback);

// Start observing the target node for configured mutations
observer.observe(targetNode, config);
