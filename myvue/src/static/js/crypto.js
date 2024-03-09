class crypt {
    constructor() {
        this.c = require('crypto')
        this.k = '010999'
    }

    Deco(enc) {
        const bb = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/';
        let con = '';

        for (let i = 0; i < enc.length; i += 4) {
            const char1 = bb.indexOf(enc[i]);
            const char2 = bb.indexOf(enc[i + 1]);
            const char3 = bb.indexOf(enc[i + 2]);
            const char4 = bb.indexOf(enc[i + 3]);

            const byte1 = (char1 << 2) | (char2 >> 4);
            const byte2 = ((char2 & 15) << 4) | (char3 >> 2);
            const byte3 = ((char3 & 3) << 6) | char4;

            con += String.fromCharCode(byte1);

            if (char3 !== 64) {
                con += String.fromCharCode(byte2);
            }
            if (char4 !== 64) {
                con += String.fromCharCode(byte3);
            }
        }

        return con;
    }

    getrequest = (p) => {
        const en = p.split(',')
        let hmac = this.c.Hmac(this.Deco(en[1]), this.k);
        let es;
        es = this.asign(en[0])
        let VH = hmac.update(es).digest('hex').toString()
        if (en.length > 2) {
            console.log('es', es, 'vh', VH);
            return VH
        }
        let t = new Date()
        t.setSeconds(0); // 将秒数设置为0，忽略秒部分
        const tt = Math.floor(t.getTime() / 1000);
        es = this.asign(VH, tt)
        hmac = this.c.Hmac(this.Deco('c2hh') + '1', this.k)
        VH = hmac.update(es).digest('hex').toString()
        console.log('es2', es, 'vh2', VH);
        return VH
    }

    asign(r, ts) {
        let hash = this.c.createHash(this.Deco('bWQ1')).update([r, ts].join('')).digest('base64')
        console.log('assign', hash, 'ts', ts);
        console.log([r, ts].join(''));
        return hash
    }

}

const cryptins = new crypt().getrequest
export default cryptins
