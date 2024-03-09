const channel = new BroadcastChannel('user')

/**
 * Sends a message with the given type and content.
 *
 * @param {type} type - The type of the message.
 * @param {type} content - The content of the message.
 * @return {undefined}
 */
export function sendMsg(type, content) {
  channel.postMessage({
    type,
    content
  })
}

export function listenMsg(callback) {
  channel.addEventListener('message', (e) => {
    callback(e)
  })
}

export function revlistenMsg() {
  channel.removeEventListener('message')
}
