* package org.appinventor;
import com.google.appinventor.components.runtime.HandlesEventDispatching;
import com.google.appinventor.components.runtime.EventDispatcher;
import com.google.appinventor.components.runtime.Form;
import com.google.appinventor.components.runtime.Component;
import com.google.appinventor.components.runtime.Label;
import com.google.appinventor.components.runtime.Button;
class Screen1 extends Form implements HandlesEventDispatching {
  private Label Label1;
  private Button Button1;
  protected void $define() {
    this.AppName("Test");
    this.Title("Screen1");
    Label1 = new Label(this);
    Label1.Text("Text for Label1");
    Button1 = new Button(this);
    Button1.Text("Click");
    EventDispatcher.registerEventForDelegation(this, "ClickEvent", "Click" );
  }
  public boolean dispatchEvent(Component component, String componentName, String eventName, Object[] params){
    if( component.equals(Button1) && eventName.equals("Click") ){
      Button1Click();
      return true;
    }
    return false;
  }
  public void Button1Click(){
    Label1.Text("Distance");
  }
}*