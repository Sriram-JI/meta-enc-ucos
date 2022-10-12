FILESEXTRAPATHS_prepend := "${THISDIR}/${PN}:"

SRC_URI += "file://0001-Added-AES-cmd.patch file://0002-Load-Ucos.patch file://0003-Load-Encrypted-Ucos.patch "


SRC_URI += "file://key.key \
	   file://zImage"
	    
RDEPENDS_${PN} += "bash"

do_deploy_append() {
	install -d 0755 ${DEPLOYDIR}
   	install -D -m 0755  ${WORKDIR}/key.key ${DEPLOYDIR}
   	install -D -m 0755  ${WORKDIR}/zImage ${DEPLOYDIR}
   
}
